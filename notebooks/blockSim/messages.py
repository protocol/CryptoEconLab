#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 21:05:38 2022

@author: juan
"""

from dataclasses import dataclass
import numpy as np
import uuid
import pandas as pd



def message(gasUsed:float,
gasLimit:float,
bid:float,
baseFee:float,
tip:float,
Class:str,
sender:str,
time:float,
cycle:int,
subcycle:int,
partition:int=None):
    
    
    m={'gasUsed':gasUsed,
    'gasLimit':gasLimit,
    'bid':bid,
    'baseFee':baseFee,
    'tip':tip,
    'Class':Class,
    'sender':sender,
    'time':time,
    'cycle':cycle,
    'subcycle':subcycle,
    'partition':partition,
    'profit':min(bid,baseFee+tip)}
    return m
    
    
    
    
    
class Mpool:
    ''' creates a Mpool object'''
    
    def __init__(self):
        self.t=0
        self.messages=[]
        self.MpoolSize=5000
        
        
    def resample(self):
        
        
        n=len(self.messages)
        if n>=self.MpoolSize:
            self.messages=list(np.random.choice(self.messages,size=self.MpoolSize,replace=False))
    
    def addMessage(self,m:message):
        '''
        Adds a message to the Mpool

        Parameters
        ----------
        m : message
            a message class, see above

        Returns
        -------
        None.

        '''
        self.messages.append(m)
    
    def remove(self,m:message):
        '''
        removes a message to the Mpool

        Parameters
        ----------
        m : message
            a message class, see above

        Returns
        -------
        None.

        '''
        self.messages.remove(m)
        
    def getClassi(self,i):
        '''
        returns Mt^i={m in Mt |  c(m)=i}

        Parameters
        ----------
        i : int
            message class

        Returns
        -------
        mi : list
            returns Mt^i={m in Mt |  c(m)=i}.

        '''
        M=self.messages
        mi=[m for m in M if m.group==i]
        return mi
        
    def getDemand(self,i):
        '''
        gets demand plot for class i at current time

        Parameters
        ----------
        i : TYPE
            DESCRIPTION.

        Returns
        -------
        res : TYPE
            DESCRIPTION.

        '''
        #gets 
        mi=self.getClassi(i)
        prices=np.sort([m['value'] for m in mi])
        
        demand=[]
        demand=[np.sum([m['gas'] for m in mi if m['value']>=p]) for p in prices]

        # for p in prices:
        #     demand=[np.sum(m.gas for m in mi if m.value>=p) for p in prices]
        #     demand.append(np.sum(aux))
        
        
        res={
            'prices':prices,
            'demand':demand,
            'class':i,
            'time':self.t
            
            }
        
        return res

    def toDF(self):
        
        return pd.DataFrame(self.messages)
        
        
        
        


# #creates a random Mpool
# Nmessages=10000
# Mt=Mpool()
# Nc=4
# muV,sigV=2,3
# muG,sigG=3,3

# import datetime
# for i in range(Nmessages):
#     m=message( gasUsed=10+2*np.random.random(),
#         gasLimit=10+2*np.random.random(),
#         bid=np.random.random(),
#         baseFee=100,
#         tip=np.random.random(),
#         Class=np.random.randint(4),
#         sender=np.random.randint(100),
#         time=datetime.datetime.now(),
#         cycle=np.random.randint(48))
    
#     Mt.addMessage(m)
    
# mdf=Mt.toDF() 
# i=np.random.randint(Nc)
# res=Mt.getDemand(i=i)        
        
# import matplotlib.pyplot as plt
# import matplotlib
# font = {'family' : 'serif',
#     'size'   : 32}
# matplotlib.rc('font', **font)


# fig,ax=plt.subplots(1,2,figsize=(16,9))
# ax[0].plot(res['prices'],res['demand'])
# ax[0].set_xlabel('price')
# ax[0].set_ylabel('demand of class i={}'.format(i))   
# ax[1].loglog(res['prices'],res['demand'])
# ax[1].set_xlabel('price')
# ax[1].set_ylabel('demand of class i={}'.format(i))   
        
# plt.tight_layout()
