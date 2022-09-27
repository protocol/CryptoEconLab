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

#%%
def dataPreprocess(height:int,secretString:str or None):



    if secretString is None:
        db=None
        #connects to sentinel
    else:
        print('connecting to sentinel..')
        db = utils.connect_to_sentinel(secret_string=secretString)
        
        
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
   # list_core_devs=list(pd.read_csv('datasets/listOfCoreDevs.csv'))
    list_core_devs = []


    
    #gets list of votes
    
    print('getting list of votes...')
    try:
    
        votes=Votes() ; votes.update()
        listVotes=votes.votes
        N_votes=len(listVotes)
        
        #deduplicates votes
        #listVotes=[listVotes.iloc[n] for n in range(N_votes) if listVotes['address'].iloc[n][:2]!='f0']

        listVotes=pd.DataFrame(listVotes)
        listVotes.to_csv('datasets/listOfVotes.csv')
        
    except:
        print('cou;dnt connect to vote db, reading stored')
        listVotes=pd.read_csv('datasets/listOfVotes.csv')


    try: 
        print('getting list of mappings...')
        
        list_of_mappings=pd.read_csv('datasets/longShort.csv')
    except:
        import os
        from tqdm import tqdm
        
        print('building list of mappings...')

        
        voters=list(listVotes['signerAddress'])
        list_of_mappings=[]
        
        for i in tqdm(range(len(voters))):
            # import pdb
            # pdb.set_trace()
            cmd='/usr/local/bin/lotus state lookup   '+voters[i]
            id_short=os.popen(cmd).read()[:-1]
            list_of_mappings.append(id_short)
        list_of_mappings=pd.DataFrame({'long':voters,
                                       'short':list_of_mappings})
        
        
        list_of_mappings.to_csv('datasets/longShort.csv')
    
    print('getting miner balances...')
    list_of_balances=pd.read_csv('datasets/miner_balances.csv')

        
                                      

        
        


    results={'deals':listDeals,
             'miners':miner_info,
             'addresses':list_addresses,
             'votes':listVotes,
             'core':list_core_devs,
             'powers':list_powers,
             'longShort':list_of_mappings,
             'balances':list_of_balances
             }
    
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
    
    