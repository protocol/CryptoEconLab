"""
This file contains various ways to model PSD Gas in Filecoin
"""

import pandas as pd
import numpy as np
import sklearn.preprocessing as skp
import scipy.stats

import mechafil.data_spacescope as dss

import pyflux as pf
import pmdarima as pm
from pmdarima.arima.utils import ndiffs
from patsy import dmatrices

auth='/Users/kiran/code/auth/kiran_spacescope_auth.json'
sso = dss.SpacescopeDataConnection(auth)

def get_gas_data_spacescope(start_date, end_date):
        
    df_gas = sso.spacescope_query(
        start_date,
        end_date,
        url_template='https://api.spacescope.io/v2/gas/daily_gas_usage_in_units?end_date=%s&start_date=%s'
    )
    df_gas['date'] = pd.to_datetime(df_gas['stat_date']).dt.date
    return df_gas

def get_training_data(start_date, end_date):
    """
    This function returns a dataframe with the following columns:
    - date
    - fpr (filplus rate)
    - day_onboarded_deal_power
    - network_qa_rb_ratio - the total ratio of QA to RB power on the network
    - gas usage
    """
    gas_df = get_gas_data_spacescope(start_date, end_date)
    df_power_onboard = sso.query_spacescope_daily_power_onboarded(
        start_date,
        end_date
    )
    df_power_cumulative = sso.query_spacescope_power_stats(
        start_date, 
        end_date
    )
    # merge the dataframes
    tdf = pd.merge(gas_df, df_power_onboard, on='date', how='outer')
    tdf = pd.merge(tdf, df_power_cumulative, on='date', how='outer')
    
    tdf['fpr'] = (tdf['day_onboarded_qa_power_pib'] - tdf['day_onboarded_rb_power_pib'])/tdf['day_onboarded_qa_power_pib']
    tdf['day_onboarded_deal_power'] = (tdf['day_onboarded_qa_power_pib'] - tdf['day_onboarded_rb_power_pib'])/9
    tdf['network_qa_rb_ratio'] = tdf['total_qa_power_eib'] / tdf['total_raw_power_eib']

    # add in precommitx and provecommitx gas fields
    tdf['precommitx_sector_gas_used'] = tdf['precommit_sector_gas_used'] + tdf['precommit_sector_batch_gas_used']
    tdf['provecommitx_sector_gas_used'] = tdf['provecommit_sector_gas_used'] + tdf['provecommit_aggregate_gas_used']
    
    return tdf

# patsy style formulas
gas2kwargs = {
    'psd': { # works OK
        'x_col': 'publish_storage_deals_gas_used',
        'y_cols': ['day_onboarded_deal_power', 'network_qa_rb_ratio'],
        'formula': 'publish_storage_deals_gas_used~1+day_onboarded_deal_power+network_qa_rb_ratio',
    },
    'precommitx': {  # can be improved
        'x_col': 'precommitx_sector_gas_used',
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 'network_qa_rb_ratio'],
        'formula': 'precommitx_sector_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio',
    },
    'precommit': {  # can be improved
        'x_col': 'precommit_sector_gas_used',
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib'],
        'formula': 'precommit_sector_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib',
    },
    'provecommitx': { # works OK
        'x_col': 'provecommitx_sector_gas_used',
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 'network_qa_rb_ratio'],
        'formula': 'provecommitx_sector_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio',
        
    },
    'total': {  # can be improved
        'x_col': 'total_gas_used',
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 'network_qa_rb_ratio'],
        'formula': 'total_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio',
    }
}

class PyfluxWrapper:
    def __init__(self, x_col, y_cols, formula, log_after_scaler=False):
        self.xcol = x_col
        self.ycols = y_cols
        self.formula = formula

        self.all_cols = [x_col] + y_cols

        self.normalizer = None
        self.model = None
        self.log_after_scaler = log_after_scaler
        
        self.t = None

    def normalize(self, df):
        for c in df.columns:
            if 'date' in c:
                self.t = pd.to_datetime(df[c]).dt.date
                break
        
        # subset to columns in formula only
        df = df[self.all_cols]

        if self.normalizer is None:
            if self.log_after_scaler:
                # since we are doing a log, we do a scaling that keeps data between 0 and 1
                # could choose betwen min/max and quantile. start w/ min/max
                self.normalizer  = skp.MinMaxScaler().set_output(transform='pandas')
                # self.normalizer  = skp.QuantileTransformer().set_output(transform='pandas')
            else:
                self.normalizer = skp.StandardScaler().set_output(transform='pandas')
            df_normalized = self.normalizer.fit_transform(df)
        else:
            df_normalized = self.normalizer.transform(df)

        if self.log_after_scaler:
            # df_normalized[self.x_col] = np.log1p(df_normalized[self.x_col])
            df_normalized = np.log1p(df_normalized)

        return df_normalized
    
    def forecast(self, test_df, num_mc=500):
        # normalize the data the same way we normalized the train
        test_df_normalized = self.normalize(test_df)

        dep_var = self.formula.split("~")[0]
        oos_data = test_df_normalized.copy()

        # TODO: if dep_var not in the inputted dataframe, can fill with zeros

        oos_data[dep_var] = oos_data[dep_var].replace(np.nan, 0)
        _, X_oos = dmatrices(self.formula, oos_data, return_type="dataframe")  
        h = len(test_df_normalized)
        X_pred = X_oos
        if self.model is not None:
            sim_vector = self.model._sim_prediction_bayes(h, np.asarray(X_pred), num_mc) # shape = [h, num_mc]
            sim_vector = sim_vector.T # shape = [num_mc, h]
            
            y_pred = np.zeros_like(sim_vector)

            for ii in range(sim_vector.shape[0]):
                tmp_df = X_oos.copy()
                tmp_df[self.x_col] = sim_vector[ii,:]
                
                if self.log_after_scaler:
                    # tmp_df[self.x_col] = np.expm1(tmp_df[self.x_col])
                    tmp_df = np.expm1(tmp_df)
                # make sure column order is correct
                tmp_df = tmp_df[self.all_cols]
                
                # we can take index 0 directly here b/c x_col is the first column (see constructor)
                y_pred[ii,:] = self.normalizer.inverse_transform(np.asarray(tmp_df))[:, 0]
            
            return y_pred
        else:
            raise ValueError("Model not yet fitted!")


class ArimaxGasModel(PyfluxWrapper):
    def __init__(self, gas_type='psd', log_after_scaler=False):
        kwargs = gas2kwargs[gas_type]
        self.formula = kwargs['formula']
        self.x_col = kwargs['x_col']
        self.y_cols = kwargs['y_cols']

        super(ArimaxGasModel, self).__init__(self.x_col, self.y_cols, self.formula, log_after_scaler=log_after_scaler)

        self.normalizer = None
        self.model = None
        self.log_after_scaler = log_after_scaler

    def train_model(self, train_df):
        # normalize the data
        tdf = self.normalize(train_df)

        # find optimal arima model parameters
        modl = pm.auto_arima(tdf[self.x_col].values, 
                        X=tdf[self.y_cols].values,
                        start_p=1, start_q=1, start_P=1, start_Q=1,
                        max_p=5, max_q=5, max_P=5, max_Q=5, seasonal=True,
                        stepwise=True, suppress_warnings=True, D=10, max_D=10,
                        error_action='ignore')
        optimal_ar = modl.order[0]
        optimal_ma = modl.order[2]
        optimal_integ = modl.order[1]

        prior = pf.Normal()  # if we use the normalizer above, then this is appropriate
        self.model = pf.ARIMAX(
            data=tdf, 
            formula=self.formula,
            ar=optimal_ar, 
            integ=optimal_integ, 
            ma=optimal_ma, 
            family=prior
        )

        # fit the model w/ metropolis hastings
        result = self.model.fit('M-H', nsims=20000)
    
        return result
    
    
        
class GasxGasModel(PyfluxWrapper):
    def __init__(self, gas_type='psd', log_after_scaler=False):
        kwargs = gas2kwargs[gas_type]
        self.formula = kwargs['formula']
        self.x_col = kwargs['x_col']
        self.y_cols = kwargs['y_cols']

        super(GasxGasModel, self).__init__(self.x_col, self.y_cols, self.formula, log_after_scaler=log_after_scaler)

        self.normalizer = None
        self.model = None
        self.log_after_scaler = log_after_scaler

    def train_model(self, train_df):
        # normalize the data
        tdf = self.normalize(train_df)

        # find optimal arima model parameters
        modl = pm.auto_arima(tdf[self.x_col].values, 
                        X=tdf[self.y_cols].values,
                        start_p=1, start_q=1, start_P=1, start_Q=1,
                        max_p=5, max_q=5, max_P=5, max_Q=5, seasonal=True,
                        stepwise=True, suppress_warnings=True, D=10, max_D=10,
                        error_action='ignore')
        optimal_ar = modl.order[0]
        optimal_ma = modl.order[2]
        optimal_integ = modl.order[1]

        prior = pf.Normal()  # if we use the normalizer above, then this is appropriate
        self.model = pf.GASX(
            data=tdf, 
            formula=self.formula,
            ar=optimal_ar, 
            sc=optimal_ma, 
            family=prior,
            integ=optimal_integ,
        )

        # fit the model w/ metropolis hastings
        result = self.model.fit('M-H', nsims=20000)
    
        return result