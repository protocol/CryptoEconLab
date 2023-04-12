#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 08:55:33 2023

@author: juan
"""

import numpy as np
import matplotlib.pyplot as plt
from survival import *
import requests
import datetime
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import pandas as pd
from scipy import stats


today = datetime.date.today()
startDate = today - datetime.timedelta(90)

url = f"https://api.spacescope.io/v2/storage_provider/power?state_date=2023-02-01"

payload = {}
headers = {
    'authorization': 'Bearer ghp_kyBnhDylmTocfnsNuhDRLQSQBfoPscdoEBYa'
}

response = requests.request("GET", url, headers=headers, data=payload)
rhos = pd.DataFrame(response.json()['data'])
rhos = rhos[rhos['raw_byte_power'] > 0]
rhos['power'] = rhos['quality_adj_power'] / rhos['quality_adj_power'].sum()


url = "https://api.spacescope.io/v2/storage_provider/token_balance?state_date=2023-02-01"

payload = {}
headers = {
    'authorization': 'Bearer ghp_kyBnhDylmTocfnsNuhDRLQSQBfoPscdoEBYa'
}

response = requests.request("GET", url, headers=headers, data=payload)
balance = pd.DataFrame(response.json()['data'])


df = pd.merge(rhos, balance, on='miner_id')

plt.plot(df['power'], df['balance'], '.', alpha=0.3)
plt.xlabel('relative power')
plt.ylabel('Token balance')


a, b = np.polyfit(df['power'], np.log(df['balance']), deg=1)

plt.plot(
    df['power'],
    np.exp(
        a * df['power'] + b),
    linestyle='dashed',
    color='C1',
    label=r'slope {}, intercept {}'.format(
        round(
            b,
            2),
        round(
            a,
            2)))
plt.legend()
plt.title('Balance vs relative power')
plt.xscale('log')
plt.yscale('log')
