#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  4 13:06:08 2022

@author: juan
"""

#import mpool 
import datetime
import numpy as np
import pandas as pd
import datetime
from messages import Mpool
#from Mpool import Mpool
##########################################  
#
#       Base Fee class
#
##########################################  


class basefee:
    
    def __init__(self,basefee):
        self.basefee=[basefee]
        self.MIN_BASE_FEE=100e-18 #100 attoFIL

        
    def getCurrentBaseFee(self):
        return self.basefee[-1]

    def updateBaseFee(self,gasUsed,Target):
        b_=self.getCurrentBaseFee()
        bf=b_*(1+1/8*(gasUsed-Target)/Target)
        bf=max(bf,self.MIN_BASE_FEE)
        self.basefee.append(bf)

##########################################  
#
#       Block class
#
########################################## 

class blocks:
    
    def __init__(self,target,maxBlock):
        self.target=target
        self.maxBlock=maxBlock
        self.blocks=[]
        
    def addBlock(self,M:list):
        self.blocks.append(M)
    
    def getGasUsed(self):
        B=self.blocks
        if len(B)==0:
            gu=self.target
        else:
            B=B[-1]
            gu=0
            for m in B:
                gu+=m['gasUsed']
            
        return gu
        
    
    

class Time:

    def __init__(self,time):
        
        self.time=time
        # for the cycles
        start="00:00:00"
        end="23:59:59"
        delta = datetime.timedelta(minutes=30)
        start = datetime.datetime.strptime( start, '%H:%M:%S' )
        end = datetime.datetime.strptime( end, '%H:%M:%S' )
        t = start
        cycles=[]
        while t <= end :
            cycles.append((datetime.datetime.strftime( t, '%H:%M:%S')))
            t += delta
        self.cycles=np.array(cycles)        
        self.CycleLength=datetime.timedelta(minutes=30) 
        self.epochLength=datetime.timedelta(seconds=30) 

 
    def getCycle(self):
        '''given a datetime object, returns the cycle to which it corresponds to'''
        t=self.time.strftime("%H:%M:%S")
        indx=np.argmax(self.cycles>t)
        return indx
        
    
    
    def updateTime(self):
        self.time=self.time+self.epochLength  
        
##########################################  
#
#       STATE class
#
##########################################            


class STATE(basefee,blocks,Time,Mpool):
    
    def __init__(self,bf,target,maxBlock,time):
        #instantiates parent classes
        basefee.__init__(self, bf)
        blocks.__init__(self,target,maxBlock)
        Time.__init__(self, time)        
        Mpool.__init__(self)
        
    def updateState(self,B):
        self.addBlock(B)
        self.updateTime()
        self.updateBaseFee(gasUsed=self.getGasUsed(),Target=self.target)
        self.messages=[m for m in self.messages if m['partition'] is  None]
    
    def getValidMpool(self):
        vm=[m for m in self.messages if m['baseFee']>=self.getCurrentBaseFee()]
        return vm
        
        
        
    
        
        

        
        