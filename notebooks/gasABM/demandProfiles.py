#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is a function to include demand profiles
@author: juan
"""
import numpy as np
from constants import NUM_MINERS
def survival(x,a,b)->np.ndarray:
    xmin=1e-16
    s=1-1/(1+np.exp(-a*(x-b)))
    s0=1-1/(1+np.exp(-a*(xmin-b)))
    s=s/s0
    return s

class SigmoidDemand:
    
    def __init__(self,a:float,b:float,
                 Nsampler:callable,TrxDist:callable,
                 TipDistr:callable,jumpIntensity:float=0):
                
        self.a=a
        self.b=b
        self.TrxDist=TrxDist
        self.Nsampler=Nsampler
        self.TipDistr=TipDistr
        self.jumpIntensity=0
    
    def getNumberOfMessages(self,base_fee):
        
        
        jumpToZero=np.random.random()<self.jumpIntensity
        if jumpToZero:
            num_transactions=0
            print('empty!')
        else:
            num_transactions =  self.Nsampler(base_fee)
            num_transactions = int(num_transactions * survival(base_fee, self.a(), self.b()))
        return num_transactions
    
    
    def getTrxGas(self,base_fee:float):
        return  self.TrxDist(base_fee)
    
    def getTip(self,base_fee:float):
        return   self.TipDistr()*(1- survival(base_fee, self.a(), self.b()))



