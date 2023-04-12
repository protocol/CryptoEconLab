#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the module for the survival function
@author: juan
"""
import numpy as np
import matplotlib.pyplot as plt

def survival(x,a,b)->np.ndarray:
    
    s=1-1/(1+np.exp(-a*(x-b)))
    s0=1-1/(1+np.exp(-a*(1e-16-b)))

    
    
    
    #s=1/2-1*np.arctan(2*a*(x-b))/np.pi
    #s0=1/2-1*np.arctan(2*a*(1e-16-b))/np.pi
    s=s/s0
    return s

def priceFromDemand(y,D,a,b)->np.ndarray:
    
    
    #N=1/2-1*np.arctan(2*a*(1e-16-b))/np.pi
    N=1-1/(1+np.exp(-a*(1e-16-b)))
    x=b-(np.log(N*y)-np.log(D-N*y))/a

    return x
    
    

def Demand0FVM(d0,A,B):
    return A*d0**B


def totalInitialDemand(D0,A,B):
    return D0+Demand0FVM(D0,A,B)



def totalSurvival(x,dm,df,am,bm,af,bf):
    

    total=dm+df
    sm=dm*survival(x,am,bm)/total
    sf=df*survival(x,af,bf)/total

    return sm+sf
    

def totalDemand(x,dm,df,am,bm,af,bf):
    total=dm+df
    S=totalSurvival(x,dm,df,am,bm,af,bf)
    return total*S











# if __name__=='__main__':
#     x=np.logspace(-16,-7,100)
    
    
# for _ in range(100):
#     b=5e-9*10*np.random.random()
#     a=1e9*20*np.random.random()
    
#     plt.plot(x,survival(x,a,b),color='grey',alpha=0.3)
#     plt.xscale('log')    
# plt.vlines(5e-9,0,1,linestyle='dashed')
# plt.grid(True,which='both')
    

# A=5*np.random.random()
# B=0.9+0.105*np.random.random()
# DM=45e13
# DF=Demand0FVM(DM,A,B)
# DT=totalInitialDemand(DF,A,B)
# Ts=totalSurvival(x,DM,DT,a,b,a,bf=1e-10)
# plt.show()
# plt.plot(x,Ts)
# plt.xscale('log')    
# plt.vlines(5e-9,0,1,linestyle='dashed')
# plt.grid(True,which='both')
# plt.show()

# Td=totalDemand(x,DM,DT,a,b,a,bf=1e-10)
# plt.plot(x,Td)
# plt.xscale('log')    
# plt.vlines(5e-9,0,1,linestyle='dashed')
# plt.hlines(DM,x[0],x[-1])





