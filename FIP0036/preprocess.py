#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Preprocess data, this implies either downloading it or loading the following datasets:
    
    votes
    market deals
    owners
    core devs
    
    
@author: JP
"""

import datautils as utils
from votes import Votes
import pandas as pd


def dataPreprocess(height:int,sectreString:str):




    #connects to sentinel
    print('connecting to sentinel..')
    db = utils.connect_to_sentinel(secret_string=sectreString)
    #gets market deals
    print('getting list of deals...')
    listDeals=utils.get_market_deals(database=db, height=height)
    #gets miner info
    print('getting miner info...')

    miner_info=utils.get_owned_SPs(database=db,   height=height)
    #lists addresses
    print('getting miner and address info...')
    list_addresses=utils.get_addresses(database=db,   height=height)
    #lists get miner power
    print('getting miner power info...')
    list_powers=utils.get_active_power_actors(database=db,   height=height)    
    
    
    print('getting list of core devs...')
    list_core_devs=list(pd.read_csv('datasets/listOfCoreDevs.csv'))

    
    #gets list of votes
    
    print('getting list of votes...')
    
    votes=Votes() ; votes.update()
    listVotes=votes.votes

    results={'deals':listDeals,
             'miners':miner_info,
             'addresses':list_addresses,
             'votes':listVotes,
             'core':list_core_devs,
             'powers':list_powers}
    
    return results
# gets list of miner, owner, worker



if __name__=='__main__':
    HEIGHT=2162760
    results=dataPreprocess(height=HEIGHT,sectreString='SecretString.txt')
    deals=results['deals']
    votes=results['votes']
    miners=results['miners']
    addresses=results['addresses']
    core_devs=results['core']
    
    