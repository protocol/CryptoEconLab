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

from tqdm.auto import tqdm

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
    tdf['day_onboarded_deal_power'] = (tdf['day_onboarded_qa_power_pib'] - tdf['day_onboarded_rb_power_pib'])
    tdf['network_qa_rb_ratio'] = tdf['total_qa_power_eib'] / tdf['total_raw_power_eib']
    
    # add in precommitx and provecommitx gas fields
    tdf['precommitx_sector_gas_used'] = tdf['precommit_sector_gas_used'] + tdf['precommit_sector_batch_gas_used']
    tdf['provecommitx_sector_gas_used'] = tdf['provecommit_sector_gas_used'] + tdf['provecommit_aggregate_gas_used']
    tdf['total_minus_directfilp'] = tdf['total_gas_used'] - \
        (tdf['publish_storage_deals_gas_used'] + tdf['precommitx_sector_gas_used'] + tdf['provecommitx_sector_gas_used'])
    
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
