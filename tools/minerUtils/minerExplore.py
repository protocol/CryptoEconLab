#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:42:03 2022


This is a tool to get miner info using glif.




@author: Juan P. Madrigal-Cianci. CEL.
         juan.madrigalcianci@protocol.ai   
    
"""

import requests
import json
import time
import sqlalchemy as sqa
import pandas as pd
from tqdm import tqdm

def getAllMiners(filename:str=None):
    '''
    returns a list of all miner addresses§    

    Parameters
    ----------
    savefile : str, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    minerList: a list contaiinng all miners in the network

    '''
    url = "https://api.node.glif.io"
    
    payload = "{\n\"jsonrpc\": \"2.0\",\n\"method\": \"Filecoin.StateListMiners\",\n\"id\": 1,\n\"params\": [null]\n}\n"
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBbGxvdyI6WyJyZWFkIiwid3JpdGUiLCJzaWduIiwiYWRtaW4iXX0.7J3Bh0YHYlHVMdfjxDs_PUotZ3OQ7r4jQnfYG0m8isk',
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    minerList=json.loads(response.text)['result']
    
    if filename is None:
        filename='./listOfMiners.json'
    
    with open(filename, 'w') as f:
        json.dump(minerList, f)
    return minerList



def getValidMiners(secretString:str):
    '''
    
    Gets a list of valid miners, defined as those who have RBP>0

    Parameters
    ----------
    secretString : str
        connection string to sentinel

    Returns
    -------
    a dictionary with keys
    
   'miner_id': id of a given miner
   'raw_byte_power': rbp of that miner
   'quality_adj_power': qap of that miner
    
   

    '''
    
    if secretString is None:
        f=open('SecretString.txt')
        secretString=f.read()

    engine=sqa.create_engine(secretString)
    conn=engine.connect()
    query=''' SELECT * FROM "visor"."power_actor_claims"'''
    df=pd.read_sql(sql=query, con=conn)
    df['raw_byte_power']=df['raw_byte_power']/2**40 # in PiBs
    df['quality_adj_power']=df['quality_adj_power']/2**40 # in PiBs
    
    dfg=df.groupby(by='miner_id')['raw_byte_power','quality_adj_power'].sum()
    dfg=dfg[dfg['raw_byte_power']>0]
    
    
    results={
        'miner_id':list(dfg.index),
        'raw_byte_power':list(dfg['raw_byte_power']),
        'quality_adj_power':list(dfg['quality_adj_power'])

        }
    return results


def getMinerBalance(minerID:str):
    '''
    Gets miner Available balance based on their miner ID. 
    
    here: 
        
    Available Balance = Address Balance - Initial Pledged - Rewards Locked

    Parameters
    ----------
    minerID : str
        id of the miner we want to investigate. This is usually an f0 number

    Returns
    -------
    balance: int
        available balance of a given miner

    '''
    
    url = "https://api.node.glif.io"
    
    minerID='''"{}"'''.format(minerID)
    
    payload = "{\n\"jsonrpc\": \"2.0\",\n\"method\": \"Filecoin.StateMinerAvailableBalance\",\n\"id\": 1,\n\"params\": ["+minerID+",null]\n}\n"
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBbGxvdyI6WyJyZWFkIiwid3JpdGUiLCJzaWduIiwiYWRtaW4iXX0.7J3Bh0YHYlHVMdfjxDs_PUotZ3OQ7r4jQnfYG0m8isk',
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        balance=json.loads(response.text)['result']
    except:
        balance=0
    
    
    return balance


def getValidMinerInfo(filename:str=None,
                      secretString:str=None):
    '''


    returns balances for vsalid miners

    Parameters
    ----------
    filename : str, optional
        where to store a json file. The default is None.
    
    secretString:str optional
        connection string to sentinel. The default is None.

    
    

    Returns
    -------
    dict with miner id, balances, rbp and qap.

    '''
    
    if filename is None:
        filename='./minerInfo.json'
    
    miners= getValidMiners(secretString)
    balances=[]
    for mm in tqdm(miners['miner_id']):
        balances.append(getMinerBalance(mm))
    
    miners['balances']=balances
    
    
    with open(filename, 'w') as f:
        json.dump(miners, f)
    
    
    return miners
    
    
    
    



def getAllMinersBalance(filename:str=None,listOfMiners:list=None):
    '''
    Gets all balances from all miners. This will probably 
    take a huge amount of time to run

    Parameters
    ----------
    filename : str, optional
        DESCRIPTION. The default is None.
    flistOfMiners: list, optional,
        DESCRIPTION: a list of minersIds

    Returns
    -------
    a dict with keys 
        minerId: a list of miners
        balance: a list with balance in attoFIL of each miner

    '''
    
    
    #gets all miners
    
    if listOfMiners is None:
    
        print('getting list of all miners...')
        listOfMiners=getAllMiners()
    else:
        print('reading existing list of miners...')
    
    balances=[]
    
    print('getting available balances for each miner. Will take a while...')
    print('')
    for mm in tqdm(listOfMiners):
        balances.append(getMinerBalance(mm))
    results={
         'minerID':listOfMiners,
         'balance':balances
         }
    print('done!')
    if filename is None:
        filename='./listOfMinersWithBalance.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f)
    return results

if __name__=='__main__':
    miners=getValidMinerInfo('./validMiners.json')
    
     



