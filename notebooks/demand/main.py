#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:47:27 2023

@author: juan
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from getHistoricalDemand import _getGasData
import datetime
GEN_EPOCH=1598306400
START_DATE='2020-12-01'



df=_getGasData()

df=df[df['gas_limit_total']>0]
df['time']=pd.to_datetime(df['height']*30+GEN_EPOCH,unit='s')
df=df[df['time']>START_DATE]
df=df.sort_values(by='gas_limit_total')




plt.scatter(df['base_fee'], df['gas_limit_unique_total'])


plt.xlabel('base fee')
plt.ylabel('total gas limit')
