#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 08:19:22 2023

@author: juan
"""
from scipy import stats
import pandas as pd


class BlockDistr:

    def __init__(self, dataPath):
        df = pd.read_csv(dataPath)
        df['gasUsed'] = (1 + df['base_fee'].pct_change() - 1) * 8 * 5e9 + 5e9
        df.dropna()
        df = df[df['gasUsed'] <= 1e10]
        df = df[df['gasUsed'] >= 0]
        self.kernel = stats.gaussian_kde(df['gasUsed'] / 1e10)

    def sample(self):
        return self.kernel.resample(1)[0, 0]


def SampleNumberTrx():

    num_transactions = np.exp(3.58 + 0.4 * np.random.standard_normal())
    num_transactions = int(num_transactions * survival(base_fee, a, b))
