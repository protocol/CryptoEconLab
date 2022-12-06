#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 16:41:55 2022

Here we implement the cycle part of the code. each cycle consists of 60 epochs
i.e., 30 minutes. at this time, there are some SubmitWindowPost that need to be sent






@author: juan
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import utils as ut
import pdb
import datetime as dt
from actors import SP,FVM
from state import STATE
import pdb

def cycle(STATE: dict, 
          actors:dict,
          currentCycle:int,
          allPartitions:list):
    

    #########################################################################   #
    N_CYCLE=60
    miners=actors['miners']
    users=actors['users']
    #determines which partitions need to be proved here
    
    
    currentPartitions=ut.getAllPartitionsAtCycle(allPartitions,
                                             cycle=currentCycle)
        
    
    
    powers=ut.getPowers(miners)
    relPowers=powers/np.sum(powers)
    # each of these is an epoch 
    for i in range(N_CYCLE):
        
        # this is the part when messages arrive at the Mpool
        for m in miners:
            # each actor acts according to the  state and partitions, if needed.  
            m.act(STATE,currentPartitions,currentCycle,subCycle=i)
        for u in users:    
            u.act(STATE,currentCycle,subCycle=i)
        
        STATE.resample()
        #print('number of messages before {}'.format(len(STATE.messages)))
        #######################################################################
        #
        #    End Of epock. Select winning miner and pack block          
        #
        #######################################################################
    
        winningMiner=np.random.choice(miners,p=relPowers)
    
        B,STATE,tips,currentPartitions=winningMiner.packBlock(STATE,currentPartitions,miners)
        
        miners=ut.updateMiners(miners,winningMiner)
        STATE.updateState(B)
        #print('number of messages after {}'.format(len(STATE.messages)))
        #pdb.set_trace()
    
    
    penalisations=currentPartitions
    
    actors['miners']=miners
    
    #print('time per cycle {} s'.format(time.time()-t0))   
    return actors, STATE,  penalisations
            

            
if __name__=='__main__':
    df=pd.read_json('validMiners.json')
    
    
    miners=[]
    users=FVM(actorType='FVM',wealth=20*np.random.random(),IDnumber=1)
    for i in range(len(df)):
        miners.append(SP(actorType='miner'
                         ,wealth=20*np.random.random(),
                         IDnumber=i,
                         power=df['raw_byte_power'].iloc[i]*2**20))
    
    bf=1e-9
    target=5e9
    maxBlock=10e9
    actors={'miners':miners, 'users':[users]}

    time=dt.datetime.now()
    STATE=STATE(bf,target,maxBlock,time)
    allPartitions=ut.getPartitions(miners)
    
    
    for i in range(1,3):
        actors, STATE,  penalisations=cycle(STATE, 
                  actors,
                  i,
                  allPartitions)



        
