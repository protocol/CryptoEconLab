import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime 

## this is auxiliary


def getPowers(miners:list):
    ''' returns a list of powers, given a list of miners'''
    
    powers=[m.power for m in miners]        
    return powers


def getPartitions(miners:list):
    ''' returns a list of partitions that need to be sent at cycle i'''
    parts=[]
    
    for m in miners:
        
        mp=m.getPartitions()
        parts.append(mp)

    flat_list = [item for sublist in parts for item in sublist]

    return flat_list  


def getMinerPartitionsAtCycle(partitions:list,
                         minerID:str,cycle:int):
    
    
    l=partitions[partitions['id']==minerID]
    l=l[l['deadline']==cycle]
    return l


def getAllPartitionsAtCycle(partitions:list,
                             cycle:int):
    
    
    l=[p for p in partitions if p['deadline']==cycle ]
    return l


def updateMiners(miners,winningMiner):
    ''' update info on winning miner '''    
    indx=miners.index(winningMiner)
    miners[indx]=winningMiner
    return miners
    
    
def getPenalisation(allPartitions,miners,time):
    '''computes number of penlisations at the end of a given cycle'''
    penalisations=[]
    for pp in allPartitions:
        m=pp['ID']
        mm=miners[miners['ID']==m]
        penalisations.append({'ID':m,
                       'amount':mm.computePenalisation(),
                       'time':time})
        return time
        
 

    


