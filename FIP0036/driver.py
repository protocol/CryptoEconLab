#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this is the main update driver
@author: juan
"""

from groups import groups
from tqdm import tqdm
from preprocess import dataPreprocess
from counting import countVote

def recount_all():
    '''
    recounts votes

    '''
    HEIGHT = 2162760
    datasets=dataPreprocess(height=HEIGHT,sectreString='SecretString.txt')  
    list_of_votes=datasets['votes']
    N_votes=len(list_of_votes)
    signatures=[]
    deal=groups(1)
    capacity=groups(2)
    client=groups(3)
    token=groups(4)
    core=groups(5)
    groups_of_voters={
        'core':core,
        'token':token,
        'client':client,
        'capacity':capacity,
        'deal':deal
        }
    print('')
    print('begin counting...')
    print('')
    for ii in tqdm(range(N_votes)):
        vote = list_of_votes.iloc[ii]
        groups_of_voters,signatures=countVote(vote,groups_of_voters,datasets,signatures)
    GROUPS=['deal','capacity','client','token','core']

    for gr in GROUPS:
        print('###################')
        print('Counting '+str(gr))
        print('###################')
        print('')
        print('')
        try:
            groups_of_voters[gr].count()
        except:
            pass
        
        print('')
    return datasets,groups_of_voters