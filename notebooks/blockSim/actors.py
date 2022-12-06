#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the actor module. 
"""

import numpy as np
import messages
import utils as ut
class actor:

    def __init__(self,actorType:str,wealth:float,IDnumber:int):
        self.type=actorType
        self.ID=actorType+'_'+str(IDnumber).zfill(5)
        
    def getID(self):
        return self.ID
    
    def getType(self):
        return self.type
    
    def getWealth(self):
        return self.wealth



class FVM(actor):
    def __init__(self, actorType:str,wealth:float,IDnumber=int):
        super().__init__(actorType, wealth,IDnumber)
        
        
    
    def act(self,STATE,cycle,subCycle):
        '''
        

        Parameters
        ----------
        STATE : TYPE
            DESCRIPTION.
        cycle : TYPE
            DESCRIPTION.
        subCycle : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        '''
        bf=STATE.getCurrentBaseFee()
        N=self.MessagesPerEpoch(bf)
        
        gasUsed=100e6*np.random.random(N)
        gasLimit=gasUsed*(1+0.1*np.random.random(N))
        bid=bf*(1+0.1*np.random.random(N))
        time=STATE.time,

        
        for n in range(N):
            
            
            m=messages.message(gasUsed=gasUsed[n],
                               gasLimit=gasLimit[n],
                               bid=bid[n],
                               baseFee=STATE.getCurrentBaseFee(),
                               tip=np.random.random(),
                               Class=np.random.randint(4),
                               sender=self.ID,
                               time=STATE.time,
                               cycle=cycle,
                               subcycle=subCycle)
            
            
            STATE.addMessage(m)
        





    




    

    def MessagesPerEpoch(self,bf):
        return np.random.poisson(100)





    
    
class SP(actor):
    
    '''this is the storage provdier class'''
    def __init__(self, actorType:str,wealth:float,IDnumber:int,power:float):
        super().__init__(actorType, wealth,IDnumber)
        self.power=power
        N_RANDOM_SLOTS=48
        SECTORS_IN_A_PARTITION=2349
        SECTORS_IN_GB=23
        NPartitions=int(power/SECTORS_IN_A_PARTITION/SECTORS_IN_GB)
        self.wealth=wealth
        self.partitions=[]
        self.penalisationAmount=[]
        for i in range(NPartitions):
            
            self.partitions.append(
                {'id':self.ID,
                 'No':i,
                 'deadline':np.random.randint(1,N_RANDOM_SLOTS),
                 'sent':False,
                 'proved':False}
                )
        self.penalisations=[]

        
        
    def SubmitOneWindowedPost(self,STATE,gasUsed:float,
                       gasLimit:float,
                       bid:float,
                       tip:float,
                       partition:int,
                       cycle:int,
                       subcycle:int):
        
        ''' this is the code to submit exactly one partition'''        
        m=messages.message(gasUsed=gasUsed,
                           gasLimit=gasLimit,
                           bid=bid,
                           baseFee=STATE.getCurrentBaseFee(),
                           tip=tip,
                           Class='SubmitWindowedPoSt',
                           sender=self.ID,
                           time=STATE.time,
                           cycle=cycle,
                           subcycle=subcycle,
                           partition=partition)
        
    
        STATE.addMessage(m)
        indx=self.partitions.index(partition)
        self.partitions[indx]['sent']=True
        

    
    
    def act(self,STATE,currentPartitions,currentCycle,subCycle):
        
        ''' this is the action method of the SP agent. Here the agent
        decides which partitions to send'''
    
        partitionsToSend=[cp for cp in currentPartitions if cp['id']==self.ID]
        
        gasUsed=27000000*(1+0.1*np.random.random())
        gasLimit=gasUsed*(1+np.random.random())
        baseFee=STATE.getCurrentBaseFee()
        tip=np.random.random()
        bid=baseFee*(1+np.random.random())
        
        #sends all the submit Windowed Posts
        for p in partitionsToSend:
               
            self.SubmitOneWindowedPost(STATE,gasUsed,
                               gasLimit,
                               bid,
                               tip,
                               p,
                               currentCycle,
                               subCycle)
            
        
    
    

        
        
        
    def updateWealth(self,amount):
        ''' here we update the miners wealth'''
        self.wealth=self.wealth+amount
    
        
    def getPartitions(self):
        ''' here we get the partitions of that given miner'''
        return self.partitions
    

        
    def getPartitionsCurrentDeadline(self,t):
        auxParts=self.partitions
        parts=[pp for pp in auxParts if t==pp['deadline']]
        return parts
    


            
            

        
    def packBlock(self,STATE,PartitionList,miners,blockreward=20):
        
        ''' this is a sub-optimal way of packing. Since minting rewards>> block
        rewards, there's no incentive to do this '''
        
        MaxBlock=STATE.maxBlock
        mpool=STATE.getValidMpool()
        mpool.sort(key=lambda x:x['profit'])
        B=[]
        G=0
        tips=0
        
        
        
        
        for m in mpool:
            if m['gasUsed'] + G<MaxBlock:
                B.append(m)
                G+=m['gasUsed']
                tips+=m['profit']
                STATE.remove(m)
                # import pdb
                # pdb.set_trace()
                if m['partition'] is not None:
                    PartitionList.remove(m['partition'])
                    
                    
                    
        
        
        self.wealth+=blockreward+tips
        
        return B,STATE,tips,PartitionList

import pandas as pd        
df=pd.read_json('validMiners.json')


miners=[]
for i in range(len(df)):
    miners.append(SP(actorType='miner'
                     ,wealth=20*np.random.random(),
                     IDnumber=i,
                     power=df['raw_byte_power'].iloc[i]*2**20))

    
    
        
        