#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:56:09 2022

@author: juan
"""
import numpy as np
import pandas as pd
import datetime


def getBaseline(forecast_lenght):
    mainnet_start = datetime.date(2020, 10, 15)
    
    current_date = datetime.date.today()   # some of the data comes in a bit slower ... 


    end_date = current_date + datetime.timedelta(days=forecast_lenght)

    # Baseline function
    baseline_growth = float(np.log(2)/365.0)
    num_days = end_date-mainnet_start
    num_days = num_days.days
    EXA_TO_EIB = (10**18) / (2**60)
    b0 = 2.88888888
    b0_adj = b0 * EXA_TO_EIB
    baseline_df = pd.DataFrame({
        "time": pd.date_range(start=mainnet_start, freq="d", periods=num_days),
        "total_power": b0_adj * np.exp(baseline_growth*np.arange(num_days))*2**60
    })
    
    baseline_df=baseline_df.set_index('time')
    
    return baseline_df
    
    
    
    
    
    
    
    
