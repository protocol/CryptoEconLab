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
    # Note on b0
    # b0 = 2.7636
    # this value is required to match sentinel
    # it's the value we use in the digital twin and it gives correct baseline crossing date
    # it's close to the 2.77 starboard use
    # the spec value is 2.88888888
    b0 = 2.888888888
    baseline_df = pd.DataFrame({
        "time": pd.date_range(start=mainnet_start, freq="d", periods=num_days),
        "total_power": b0 * np.exp(baseline_growth*np.arange(num_days))*2**60
    })
    
    baseline_df=baseline_df.set_index('time')
    
    return baseline_df
    
    
    
    
    
    
    
    
