#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 14:21:55 2023

@author: juan
"""


import pandas as pd
import gdown
import os

def _getGasData(force=False):
    name='gasData.csv'
    isFile=os.path.isfile(name)
    
    if isFile and force!=True:
        return pd.read_csv(name)
    else:
        URL='https://drive.google.com/file/d/1qG8EdOOP7TPiL9KSZvlnZiIv6hQJBK2u/view?usp=share_link'
        output = name
        gdown.download(url=URL, output=output, quiet=False, fuzzy=True)
        df = pd.read_csv(name)
        return df


if __name__=='__main__':
    df=_getGasData()