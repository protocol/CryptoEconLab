#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the chain module. Here the word transaction and message are used 
interchangeably
@author: juan
"""
# Agent class for chain
import pandas as pd

class Chain:
    def __init__(self):
        self.transactions = []
        self.stats=[]
    
    def update(self,transactions,epoch,basefee,used,burnt):
        ''' adds interesting things to track'''
        entry={'epoch':epoch,
               'baseFee':basefee,
               'gasUsed':used,
               'gasBurnt':burnt,
               'messages':len(transactions)}
        
        self.stats.append(entry)
        self.transactions.append(transactions)
    def to_dataframe(self):
        ''' converts to a pandas df'''
        return pd.DataFrame(self.stats)
        
            
    

