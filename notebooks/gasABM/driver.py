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

############################################################
#
#
#creates user agents
#
#
############################################################
NUM_BLOCKS = 2880

############################################################
#
#
#creates miner  agents
#
#
############################################################
# Here I am defining a particular demand function for the miners
# Parameters
NUM_MINERS = 2
#1 demand function
A=1e10
BS=10**(-(9+2*np.random.random()))
lOG_N=3.58
SD_N=1
LOG_AVG_TRX_GAS=17.7
a=lambda :np.exp(np.log(A) +   np.random.standard_normal())
b =lambda : np.exp(np.log(BS) + np.random.standard_normal())
Nsampler=lambda x: np.exp(lOG_N + SD_N * np.random.standard_normal())/NUM_MINERS
TrxSampler= lambda x:  np.exp(LOG_AVG_TRX_GAS + 0.5*np.random.standard_normal())
tip_distr=lambda : 10**(-8*np.random.random())
demandProfileMiner=de.SigmoidDemand(a,b,Nsampler,TrxSampler,tip_distr,jumpIntensity=0.0)

# creates the power to all miners:
power = np.random.random(NUM_MINERS)
power = power / power.sum()


# assigns a packing strategy to each miner:
packStrats=[GreedyPack, semiGreedy]



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
NUM_USERS = 4
#1 demand function
A_U=1e8
BS_U=10**(-(9+2*np.random.random()))
lOG_N_U=6
SD_N_U=1
LOG_AVG_TRX_GAS_U=17.5
a_U=lambda :np.exp(np.log(A_U) +   np.random.standard_normal())
b_U =lambda : np.exp(np.log(BS_U) + np.random.standard_normal())
Nsampler_U=lambda x:np.exp(lOG_N_U + SD_N_U* np.random.standard_normal())/NUM_USERS
TrxSampler_U= lambda x:  np.exp(LOG_AVG_TRX_GAS_U + 0.5*np.random.standard_normal())
tip_distr=lambda : 10**(-8*np.random.random())

demandProfileUser=de.SigmoidDemand(a_U,b_U,Nsampler_U,TrxSampler_U,tip_distr,jumpIntensity=0.0)

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
res=ABM(params)
