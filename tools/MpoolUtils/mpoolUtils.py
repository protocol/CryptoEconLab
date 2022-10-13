#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 16:10:48 2022


This is a tool to get info from the Mpool using glif.
It contains two functions:
    
    MpoolQuerry:     queries the Mpool and saves/attaches to a json file 

    listenMpool:     keeps running MpoolQuerry every "freq" seconds until
                     it quits. i.e., it keeps gathering data
    
This is in the hopes that it might be useful to estimate demand, as well as
for visualizing messages that do not necessarilly get included on the chain.
    

@author: Juan P. Madrigal-Cianci. CEL.
         juan.madrigalcianci@protocol.ai   
    
"""

import requests
import json
import pandas as pd
import time


def listenMpool(filename:str=None,freq:int=10):
    '''
    listens to the Mpool every ::freq:: seconds by calling 'MpoolQuerry' with
    that frequency

    Parameters
    ----------
    filename : str or None
        location where you want to load/save the json file. If None, defaults
        to ./mpool.json
        
    freq : int, default 10
        how often to check.

    Returns
    -------
        None

    '''
    
    print("running")
    while True:
        try:
            MpoolQuerry(filename=filename)
            print('waiting...')
            time.sleep(freq)
            continue
        except:
            print('there was an error!')
            quit
            
    
def MpoolQuerry(filename:str=None)->dict:
    '''
    queries the Mpool and saves/attaches to a json file located in filename.json

    Parameters
    ----------
    filename : str or None
        location where you want to load/save the json file. If None, defaults
        to ./mpool.json

    Returns
    -------
    results : dict
        dictionary containing a list of messages in the Mpool. 
        Each message has keys:
           * gasLimit=is measured in units of gas and set by the message sender.
                It imposes a hard limit on the amount of gas 
                (i.e., number of units of gas) that a message’s execution 
                should be allowed to consume on chain
            * gasFeeCap= is the maximum price that the message sender is willing
                to pay per unit of gas (measured in attoFIL/gas unit)
            * gasPremium=  is the price per unit of gas (measured in attoFIL/gas) 
                that the message sender is willing to pay
                    (on top of the BaseFee) to “tip” the miner that
                    will include this message in a block        
                    
                    
    see https://spec.filecoin.io/systems/filecoin_vm/gas_fee/

    '''
    #------------------------------------------------------------------------
    # connects to the glif api
    #------------------------------------------------------------------------
    
    url = "https://api.node.glif.io"
    
    payload = "{\n\"jsonrpc\": \"2.0\",\n\"method\": \"Filecoin.MpoolPending\",\n\"id\": 1,\n\"params\": [null]\n}\n"
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBbGxvdyI6WyJyZWFkIiwid3JpdGUiLCJzaWduIiwiYWRtaW4iXX0.7J3Bh0YHYlHVMdfjxDs_PUotZ3OQ7r4jQnfYG0m8isk',
      'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    trxArray=json.loads(response.text)['result']
    
    
    #------------------------------------------------------------------------
    # checks whether the file exists. If it does, it loads it, otherwise, 
    # preallicates
    #------------------------------------------------------------------------

    if filename is None:
        filename='./Mpool.json'
    
    try:
        f = open(filename)
        
        results = json.load(f)
        print('file '+filename+' found. attaching...')
        gasLimit=results['gasLimit']
        gasFeeCap=results['gasFeeCap']
        gasPremium=results['gasPremium']
        CID=results['CID']
        
        N_old_entries=len(CID)
        
    except:
        print('file '+filename+' not found. creating...')

        gasLimit=[]
        gasFeeCap=[]
        gasPremium=[]
        CID=[]
        N_old_entries=0
    #------------------------------------------------------------------------
    # iterates over all trxs and extracts relevant info
    #------------------------------------------------------------------------
    N=len(trxArray)


    for i in range(N):
        
        aux=trxArray[i]['Message']
        gasLimit.append(int(aux['GasLimit']))
        gasFeeCap.append(int(aux['GasFeeCap']))
        gasPremium.append(int(aux['GasPremium']))
        CID.append(aux['CID']['/'])
    
    results={'gasLimit':gasLimit,
             'gasFeeCap':gasFeeCap,
             'gasPremium':gasPremium,
             'CID':CID}
    #------------------------------------------------------------------------
    # removes duplicated entries by CID
    #------------------------------------------------------------------------
    df=pd.DataFrame(results)
    df=df.drop_duplicates(subset=['CID'])
    N_new=len(df)
    results=df.to_dict(orient='list')
    #------------------------------------------------------------------------
    # exports as json file
    #------------------------------------------------------------------------
    with open(filename, 'w') as f:
        json.dump(results, f)
    
    
    
    
    print('found {} new entries.'.format(N_new-N_old_entries))
    print('total number of entries is {}'.format(N_new))

    return results
        

if __name__=='__main__':
    FILENAME='./Mpool.json'
    # import os
    # res=MpoolQuerry(FILENAME)
    # os.system('rm '+FILENAME)
    listenMpool(FILENAME)
    



