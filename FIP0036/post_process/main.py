#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
this is the main file to run
@author: juan
"""

from groups import groups
from tqdm import tqdm
from preprocess import dataPreprocess
from counting import countVote
import pandas as pd


def run(export_path:str):
    
    '''
    runs the post-processing code. results get exported to export_path
    
    Parameters
    ----------
    export_path : str
        where to export the results to
    
    Returns
    -------
    None, but stores csvs with raw votes, processed votes and tallied votes
    in export_path
    
    
    '''
    #
    HEIGHT = 2162760
    #####################################################################################
    #
    #               gets relevant datasets
    #
    ####################################################################################
    # gets relevant datasets
    datasets=dataPreprocess(height=HEIGHT,secretString='SecretString.txt')  
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
    #####################################################################################
    #
    #               main loop
    #
    ####################################################################################
    
    
    for ii in tqdm(range(N_votes)):
        vote = list_of_votes.iloc[ii]
        groups_of_voters,signatures=countVote(vote,groups_of_voters,datasets,signatures)
    GROUPS=['deal','capacity','client','token','core']
    
    
    #####################################################################################
    #
    #               displays tallied votes
    #
    ####################################################################################
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
    
    #####################################################################################
    #
    #              exports
    #
    ####################################################################################    
    all_votes=[]
    tallied=[]
    
    
    for gr in groups_of_voters:
        all_votes.append(groups_of_voters[gr].listVotes)
            
        try:
            tt=groups_of_voters[gr].tally
            tt['id']=groups_of_voters[gr].groupName
        except:
            tt={'Approve': 0,
             'Reject':0,
             'id': groups_of_voters[gr].groupName}
            
            
        tallied.append(tt)
        
    all_votes_df=pd.DataFrame(all_votes)
    tallied=pd.DataFrame(tallied)
    
    all_votes_df.to_csv(export_path+'/all_votes.csv')
    list_of_votes.to_csv(export_path+'/raw_votes.csv')
    tallied.to_csv(export_path+'/tallied_votes.csv')
    signatures.to_csv(export_path+'/signatures.csv')

    
    
    
if __name__=='__main__':
    import os
    file_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.abspath(os.path.join(file_dir, "..", "Public_Data"))
    run(export_path=output_dir)
    
