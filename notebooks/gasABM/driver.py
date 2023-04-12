#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 12:28:06 2023

@author: juan
"""

import numpy as np
from constants import *
from transaction import Transaction
from mempool import Mempool
from user import User
from miner import Miner
from baseFee import BaseFee
import matplotlib.pyplot as plt
from tqdm import tqdm
from blockStrategies import *
import demandProfiles as de
from ABM import ABM
def survival(x,a,b)->np.ndarray:
    xmin=1e-16
    s=1-1/(1+np.exp(-a*(x-b)))
    s0=1-1/(1+np.exp(-a*(xmin-b)))
    s=s/s0
    return s

############################################################
#
#
#creates user agents
#
#
############################################################
NUM_BLOCKS = 2880
M=1
bf=np.zeros((M,NUM_BLOCKS+1))
g=np.zeros((M,NUM_BLOCKS))
for i in range(M):
    ############################################################
    #
    #
    #creates miner  agents
    #
    #
    ############################################################
    # Here I am defining a particular demand function for the miners
    # Parameters
    NUM_MINERS = 1
    #1 demand function
    A=10**((11+0.3*np.random.standard_normal()))
    BS=10**(-(10+np.random.standard_normal()))
    lOG_N=np.log(58)
    LOG_AVG_TRX_GAS=18.
    a=lambda :np.exp(np.log(A) +   np.random.standard_normal())
    b =lambda : np.exp(np.log(BS) + np.random.standard_normal())
    Nsampler=lambda x,a,b: int(np.random.poisson(np.exp(lOG_N)*survival(x, a, b))/NUM_MINERS )
    TrxSampler= lambda x:  np.exp(LOG_AVG_TRX_GAS + np.random.standard_normal())
    tip_distr=lambda : 10**(-8*np.random.random())
    demandProfileMiner=de.nhPoisson(a,b,Nsampler,TrxSampler,tip_distr,jumpIntensity=0.01)
    
    # creates the power to all miners:
    power = np.random.random(NUM_MINERS)
    power = power / power.sum()
    
    
    # assigns a packing strategy to each miner:
    packStrats=[feeAversePack]
    
    
    
    # creates agents
    miners = [Miner('M'+str(i), INITIAL_BALANCE, power[i],
                    packStrategy=packStrats[i%2],demandProfile=demandProfileMiner)
              for i in range(NUM_MINERS)]
    
    ############################################################
    #
    #
    #creates user agents
    #
    #
    ############################################################
    NUM_USERS = 0
    #1 demand function
    A=10**((12+0.3*np.random.standard_normal()))
    BS=10**(-(12+np.random.standard_normal()))
    lOG_N=np.log(58)
    LOG_AVG_TRX_GAS=18.
    a=lambda :np.exp(np.log(A) +   np.random.standard_normal())
    b =lambda : np.exp(np.log(BS) + np.random.standard_normal())
    Nsampler=lambda x,a,b: int(np.random.poisson(np.exp(lOG_N)*survival(x, a, b))/NUM_MINERS )
    TrxSampler= lambda x:  np.exp(LOG_AVG_TRX_GAS + np.random.standard_normal())
    tip_distr=lambda : 10**(-8*np.random.random())
    demandProfileUser=de.nhPoisson(a,b,Nsampler,TrxSampler,tip_distr,jumpIntensity=0.02)
    
    users = [User(i, INITIAL_BALANCE,demandProfileUser) for i in range(NUM_USERS)]
    
    ############################################################
    #
    #
    #   Defines some missing parameters
    #
    #
    ############################################################
    mpoolSize=np.zeros(NUM_BLOCKS)
    gu=np.zeros(NUM_BLOCKS)
    base_fee = INITIAL_BASE_FEE
    mempool = Mempool()
    R=18.2
    params={'miners':miners,
            'users':users,
            'mempool':mempool,
            'power':power,
            'numBlocks':NUM_BLOCKS,
            'basefee':base_fee,
            'R':R}
    

############################################################
#
#
#  runs simulation
#
#
############################################################

    res=ABM(params,plots=False)
    bf[i]=res['basefee']
    g[i]=res['gasUsed']


#%%
for i in range(M):
    if i==0:
        plt.plot(bf[i],color='grey',label='realisation',alpha=0.1)
    else:
        plt.plot(bf[i],color='grey',alpha=0.1)

plt.yscale('log')
plt.plot(bf.mean(0),label='mean path')
plt.ylabel('Base fee (FIL/gas unit)')
plt.xlabel('Epoch')
plt.legend()
plt.title('Base fee paths')
plt.show()
N=np.random.poisson(5,NUM_BLOCKS)

burnt=np.array([np.sum(N*bf[j,:-1]*g[j]) for j in range(M)])

plt.title('Histogram of burn tokens')
plt.hist(burnt[burnt<1e4],density=True)
plt.xlabel('FIL burnt, per day')
plt.ylabel('density')
plt.xlim([0,1e4])


QoI=bf.mean(1)>1e-10

print('mean {} +- 95%SE {}'.format(np.mean(QoI),1.96*np.std(QoI)/np.sqrt(M)))


QoI=[any(bf[i,:]<1e-15) for i in range(M)]

print('mean {} +- 95%SE {}'.format(np.mean(QoI),1.96*np.std(QoI)/np.sqrt(M)))



