#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 18:45:16 2022

This is a MWE to test the MpoolUtils.py script

@author: juan
"""

from mpoolUtils import MpoolQuerry
import pandas as pd
import matplotlib.pyplot as plt


# gets a list of messages in the Mpool at the current time
messages=MpoolQuerry(filename='test.json')
# converts messages to a pandas dataframe and shows their head
df=pd.DataFrame(messages)
print(df.head())


plt.loglog(df['gasFeeCap'],df['gasLimit'],'.')
plt.title(' log-scale plot of gasLimit Vs. gasFeeCap')
plt.xlabel('log(gasFeeCap)')
plt.ylabel('log(gasLimit)')
plt.show()

import os
os.system('rm test.json')