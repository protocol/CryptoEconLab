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

import statsmodels.api as sm
from statsmodels.distributions.empirical_distribution import ECDF, monotone_fn_inverter
from statsmodels.tsa.arima.model import ARIMA
import pyvinecopulib as pv

from scipy.interpolate import interp1d
import numpy as np
from datetime import date, timedelta, datetime
import pandas as pd
import numpy as np
import numpy.random

import sqlalchemy as sqa
from functools import reduce

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

def get_daily_gasusage_training_data(start_date, end_date):
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
    df_power_renewed = sso.get_day_renewed_power_stats(
        start_date,
        end_date, 
        end_date
    )
    df_power_cumulative = sso.query_spacescope_power_stats(
        start_date, 
        end_date,
    )
    # merge the dataframes
    tdf = pd.merge(gas_df, df_power_onboard, on='date', how='outer')
    tdf = pd.merge(tdf, df_power_cumulative, on='date', how='outer')
    tdf = pd.merge(tdf, df_power_renewed, on='date', how='outer')
    
    tdf['fpr'] = (tdf['day_onboarded_qa_power_pib'] - tdf['day_onboarded_rb_power_pib'])/tdf['day_onboarded_qa_power_pib']
    tdf['day_onboarded_deal_power'] = (tdf['day_onboarded_qa_power_pib'] - tdf['day_onboarded_rb_power_pib'])/9
    tdf['network_qa_rb_ratio'] = tdf['total_qa_power_eib'] / tdf['total_raw_power_eib']
    
    # add in precommitx and provecommitx gas fields
    tdf['precommitx_sector_gas_used'] = tdf['precommit_sector_gas_used'] + tdf['precommit_sector_batch_gas_used']
    tdf['provecommitx_sector_gas_used'] = tdf['provecommit_sector_gas_used'] + tdf['provecommit_aggregate_gas_used']
    
    return tdf

def get_basefee_spacescope(start_date, end_date):
    url_template = "https://api.spacescope.io/v2/gas/network_base_fee?end_hour=%s&start_hour=%s"
    dates_chunked = sso.chunk_dates(start_date, end_date, chunks_days=30)
    df_list = []
    for d in dates_chunked:
        dt_start = datetime.combine(d[0], datetime.min.time())
        dt_end = datetime.combine(d[1], datetime.max.time())
        chunk_start = dt_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        chunk_end = dt_end.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        url = url_template % (chunk_end, chunk_start)
        df = sso.spacescope_query_to_df(url)
        df_list.append(df)
    df_all = pd.concat(df_list, ignore_index=True)
    df_all['hour_date'] = pd.to_datetime(df_all['hour_date'])
    return df_all

def get_message_gas_economy_lily(HEIGHT=3_000_000, auth='/Users/kiran/code/auth/lily.txt'):
    FILECOIN_GENESIS_UNIX_EPOCH = 1598306400
    with open(auth) as f:
        secretString = f.read()
    
    # Try to create a connection to the database
    try:
        # Define an engine using the connection string
        engine = sqa.create_engine(secretString)
        # Establish a connection to the database
        conn = engine.connect()
    # If the connection fails, catch the exception and print an error message
    except Exception as e:
        print("Failed to connect to database")
        # Propagate the error further
        raise(e)
        
    Q = f'''
         SELECT height, base_fee
         FROM "visor"."message_gas_economy"
         WHERE height > {HEIGHT}
         ORDER BY height ASC
     '''
    df_basefee = pd.read_sql(sql=sqa.text(Q), con=conn)
    df_basefee['time'] = pd.to_datetime(df_basefee['height'].values*30 + FILECOIN_GENESIS_UNIX_EPOCH, unit='s')
    
    return df_basefee
    
# patsy style formulas
gas2kwargs = {
    'psd': { # works OK
        'x_col': 'publish_storage_deals_gas_used',
        'y_cols': ['day_onboarded_deal_power', 'network_qa_rb_ratio'],
        'formula': 'publish_storage_deals_gas_used~1+day_onboarded_deal_power+network_qa_rb_ratio',
    },
    'precommitx': {  # can be improved
        'x_col': 'precommitx_sector_gas_used',
        # 'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 'network_qa_rb_ratio'],
        # 'formula': 'precommitx_sector_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio',
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 
                   'network_qa_rb_ratio', 'total_qa_power_eib', 'total_raw_power_eib', 'fpr', 
                   'rb_renewal_rate', 'day_renewed_rb_power_pib', 'day_renewed_qa_power_pib'],
        'formula': 'precommitx_sector_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio+total_qa_power_eib+total_raw_power_eib+fpr+rb_renewal_rate+day_renewed_rb_power_pib+day_renewed_qa_power_pib',
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
        'y_cols': ['day_onboarded_rb_power_pib', 'day_onboarded_qa_power_pib', 'day_onboarded_deal_power', 
                   'network_qa_rb_ratio', 'total_qa_power_eib', 'total_raw_power_eib', 'fpr', 
                   'rb_renewal_rate', 'day_renewed_rb_power_pib', 'day_renewed_qa_power_pib'],
        'formula': 'total_gas_used~1+day_onboarded_rb_power_pib+day_onboarded_qa_power_pib+day_onboarded_deal_power+network_qa_rb_ratio+total_qa_power_eib+total_raw_power_eib+fpr+rb_renewal_rate+day_renewed_rb_power_pib+day_renewed_qa_power_pib',
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
        _, X_oos = dmatrices(self.formula, oos_data, return_type="dataframe")   # not sure why this is len(X_oos) +1 = len(test_df)
        X_pred = np.asarray(X_oos)
        h = X_pred.shape[0]
        # print(len(X_oos), len(X_pred), h, len(test_df), len(oos_data))
        if self.model is not None:
            sim_vector = self.model._sim_prediction_bayes(h, X_pred, num_mc) # shape = [h, num_mc]
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

class BivariateCopulaModel:
    def __init__(self, X):
        self.X = X
        assert self.X.shape[1] == 2
        self.U = pv.to_pseudo_obs(X)

        self.model = None
        self.is_fit = False

    def fit(self):
        # build the copula model (allow pvlib to check all parametrizations)
        self.model = pv.Bicop(data=self.U)
        # build empirical marginal distributions and densities to convert between pseudo-obs and original data space
        self.empirical_kdes = []
        self.empirical_distributions = []
        for ii in range(self.X.shape[1]):
            x = self.X[:,ii]
            density_obj = sm.nonparametric.KDEUnivariate(x)
            density_obj.fit()
            self.empirical_kdes.append(density_obj)

            ecdf_obj = ECDF(x)
            self.empirical_distributions.append(ecdf_obj)
        
        self.is_fit = True

    def simulate_pseudoobs(self, nsamp=500):
        V = self.model.simulate(nsamp)
        return V

    def _get_lo_hi(self, xvec):
        lo = min(xvec)/8
        hi = max(xvec) + np.median(xvec)/8
        return lo, hi
    
    def pobs_to_obs(self, pobs):
        # TODO: can implement interpolation to get this smoother
        
        assert pobs.shape[1] == 2

        lo, hi = self._get_lo_hi(self.X[:,0])
        uu = self.empirical_kdes[0].cdf
        x_vec = np.linspace(lo, hi, len(uu))
        lo, hi = self._get_lo_hi(self.X[:,1])
        vv = self.empirical_kdes[1].cdf
        y_vec = np.linspace(lo, hi, len(vv))
        X = np.zeros_like(pobs)
        n = pobs.shape[0]
        
        for ii in range(n):
            u, v = pobs[ii,0], pobs[ii,1]
            best_ii_u = np.argmin(np.abs(uu-u))
            best_ii_v = np.argmin(np.abs(vv-v))
            X[ii,0] = x_vec[best_ii_u]
            X[ii,1] = y_vec[best_ii_v]
        return X
        
    def conditional_distribution(self, x=None, y=None, resolution=100):
        if (x is None and y is None) or (x is not None and y is not None):
            raise ValueError('One variable must be specified at a given value to compute the conditional distribution!')
        if x is None:  # implies given y
            marginal_value_idx = 0
            conditioned_value_idx = 1
            conditioned_value = y
            conditional_fn = self.model.hfunc2  # computes P(U1<=u1|U2=u2)
        else:   # implies given x
            marginal_value_idx = 1
            conditioned_value_idx = 0
            conditioned_value = x
            conditional_fn = self.model.hfunc1  # computes P(U2<=u2|U1=u1)
            
        # the lo and hi vals are set to be slightly beyond the bounds of the data
        lo_val = min(self.X[:,marginal_value_idx])/8
        hi_val = max(self.X[:,marginal_value_idx]) + np.median(self.X[:,marginal_value_idx])/4
        marginal_var = np.linspace(lo_val, hi_val, len(self.empirical_kdes[marginal_value_idx].cdf))
        marginal_var_resampled = np.linspace(lo_val, hi_val, resolution)
        
        # this is the variable we are wanting the distribution of
        marginal_var_pseudoobs = np.linspace(0,1,resolution)
        # this is the variable we are conditioning on
        conditioned_value_pseudoobs = self.empirical_distributions[conditioned_value_idx](conditioned_value)
        conditioned_var_pseudoobs = np.ones_like(marginal_var_pseudoobs)*conditioned_value_pseudoobs

        # setup the vector for computing conditional distribution function
        if x is None:
            UV = np.vstack([marginal_var_pseudoobs, conditioned_var_pseudoobs]).T
        else:
            UV = np.vstack([conditioned_var_pseudoobs, marginal_var_pseudoobs]).T
        conditional_copula_cdf = conditional_fn(UV)
        F_cdf = np.zeros_like(conditional_copula_cdf)
        # convert the conditional CDF to the non-pseudoobs space
        # NOTE: this is an approximation of inverse-CDF, can we do better than this??
        #   can do some interpolation, for example
        for ii, k in enumerate(conditional_copula_cdf):
            best_idx = np.argmin(np.abs(self.empirical_kdes[marginal_value_idx].cdf-k))
            F_cdf[ii] = marginal_var[best_idx]

        return (marginal_var_resampled, F_cdf), (marginal_var_pseudoobs, conditional_copula_cdf)

    def sample_conditional_distribution(self, x=None, y=None, resolution=100, nsamps=500):
        (marginal_var_resampled, F_cdf), (marginal_var_pseudoobs, conditional_copula_cdf) = \
            self.conditional_distribution(x=x, y=y, resolution=resolution)

        # use the inverse transform to convert uniform RV's to the conditional distribution
        samps_vec = np.zeros(nsamps)
        for jj in range(nsamps):
            u = np.random.rand()
            best_idx = np.argmin(np.abs(F_cdf-u))
            samps_vec[jj] = marginal_var_resampled[best_idx]

        return samps_vec

class AvgBaseFeeTotalGasUsageARMAModel:
    def __init__(self, df, basefee_col='base_fee'):
        self.df = df
        self.basefee_col = basefee_col

        self.data_prepared = False

        # Filecoin specific parameters
        self.Gstar = 5e9  # the target block size in Gas Units for Filecoin
        self.epochs_per_day = 2880
        self.blocks_per_epoch = 5
        self.blocks_per_day = self.blocks_per_epoch * self.epochs_per_day

    def prepare_data(self, Gtilde_thresh=20):
        # smaller Gtilde_thresholds correspond to more filtering
        diff_basefee = np.concatenate([[0.], np.diff(self.df[self.basefee_col])])
        self.G_tilde = 8*diff_basefee/self.df[self.basefee_col]

        # some prelimenary filtering of the data
        self.G_tilde = self.G_tilde[self.G_tilde!=0]
        self.G_tilde = self.G_tilde[np.abs(self.G_tilde)<Gtilde_thresh]

        self.data_prepared = True

    def gtilde2Gt(self, gtilde):
        """
        Gtilde = (Gt-Gstar)/Gstar
        Gstar --> target block size in Gas Units
        """
        Gt = gtilde*self.Gstar + self.Gstar
        return Gt
        
    def fit(self, Gtilde_thresh=20, verbose=True):
        if not self.data_prepared:
            self.prepare_data(Gtilde_thresh=Gtilde_thresh)
            
        model = ARIMA(self.G_tilde, order=(1,0,0)) 
        model_fit = model.fit()
        if verbose:
            print(model_fit.summary())

        # convert model parameters to OU process parameters
        # Reference: https://hackmd.io/5lcDIN23SJOrWrwy8f4Hpg#First-model-gas-as-an-Ornstein-Uhlenbeck-OU-process
        alphaHat=model_fit.params[0]
        phiHat=model_fit.params[1]
        
        # QUESTION: do we use this or do we use sigma2 from the ARIMA estimation?
        gammaHat2=np.var(self.G_tilde[1:]-alphaHat-phiHat*self.G_tilde[:-1])
        h=1 # probably to be changed
        thetaHat=-1./h*np.log(phiHat)
        muHat=alphaHat/(1-phiHat)
        sigmaHat2=(-2./h)*(gammaHat2/(1-phiHat**2))*np.log(phiHat)
        sigmaHat=sigmaHat2**0.5
        sd=((0.5*sigmaHat2/thetaHat)*(1-np.exp(-2*thetaHat*h)))**0.5
        self.ou_process_params = {
            'h': h,
            'theta': thetaHat,
            'sd': sd,
            'mu': muHat,
        }

    def sample_basefee(
        self,
        ndays_per_realization=1, 
        nsamps_per_offset=10, 
        gtilde_offset_vec=None, 
        same_basefee_within_epoch=True
    ):
        if ndays_per_realization < 1:
            print('min(ndays_per_realization) must be 1 - forcing to 1 before simulating!')
            ndays_per_realization = 1
        if gtilde_offset_vec is None:
            gtilde_offset_vec = np.asarray([0])

        h = self.ou_process_params['h']
        thetaHat = self.ou_process_params['theta']
        sd = self.ou_process_params['sd']
        muHat = self.ou_process_params['mu']
        
        gtilde = []
        basefee = []
        for ii, gtilde_offset in enumerate(gtilde_offset_vec):
            for jj in range(nsamps_per_offset):
                niter_per_loop = int(self.blocks_per_day*ndays_per_realization)
                
                G_tilde_vec = np.zeros(niter_per_loop+1)
                basefee_vec = np.zeros_like(G_tilde_vec)
                # choose random values for this
                random_idx = np.random.randint(len(self.df))
                basefee_vec[0] = self.df[self.basefee_col].iloc[random_idx]
                basefee_vec[1] = basefee_vec[0]  # hmm .... 
                G_tilde_vec[0] = np.random.rand()*2 - 1 # we know Gtilde should be between -1 and 1
                
                for n in range(1,niter_per_loop):
                    g_tilde_sample = G_tilde_vec[n-1]*np.exp(-thetaHat*h)+muHat*(1-np.exp(-thetaHat*h)) +sd*np.random.standard_normal()
                    g_tilde_scaled = np.clip((g_tilde_sample + gtilde_offset)/2, -1, 1)  # negative offset means less gas usage, positive means more
                    G_tilde_vec[n] = g_tilde_scaled
    
                    # this simulates that all blocks within the same epoch have the same base-fee, which I think makes sense.
                    # however, double check w/ JP
                    if (not same_basefee_within_epoch) or (same_basefee_within_epoch and (n % self.blocks_per_epoch == 0)):
                        basefee_vec[n+1]=max(basefee_vec[n]*(1+G_tilde_vec[n]/8), 100*1e-18) # max for ensuring base_fee doesn't go to 0
                    else:
                        basefee_vec[n+1] = basefee_vec[n]

                # the first sample is the seed
                gtilde.append(G_tilde_vec[1:])
                basefee.append(basefee_vec[1:])
        return np.concatenate(basefee), np.concatenate(gtilde)

    ## convenience functions
    def sample_basefee_avgdaily_totalgas_sumdaily(
        self,
        ndays_per_realization=1, 
        nsamps_per_offset=10, 
        gtilde_offset_vec=None, 
        same_basefee_within_epoch=True
    ):
        basefee, gtilde = self.sample_basefee(
            ndays_per_realization=ndays_per_realization, 
            nsamps_per_offset=nsamps_per_offset, 
            gtilde_offset_vec=gtilde_offset_vec, 
            same_basefee_within_epoch=same_basefee_within_epoch
        )
        assert len(basefee) == len(gtilde)
        # average base fee per day
        l = int(len(basefee)//self.blocks_per_day * self.blocks_per_day)
        basefee = basefee[0:l]
        gtilde = gtilde[0:l]
        basefee_avg_day = basefee.reshape(-1,self.blocks_per_day).T.mean(axis=0)
        gt = self.gtilde2Gt(gtilde)
        totalgas_day = gt.reshape(-1,self.blocks_per_day).T.sum(axis=0)
    
        return basefee_avg_day, totalgas_day

