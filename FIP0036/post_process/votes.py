#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script pings the real-live voter data and retrieves votes


@author: JP, juan.madrigalcianci@protocol.ai"""


import json
import pandas as pd
from urllib.request import urlopen
from datetime import datetime
pd.options.mode.chained_assignment = None  # default='warn'

class Votes:
    '''
    class to ping the votes
    '''
    
    def __init__(self):
        self.URL='https://api.filpoll.io/api/polls/16/view-votes'
        self.response=urlopen(self.URL)
        
    def getVotes(self):
        '''
        Retrieves an updated list of votes as a pandas dataframe on
        self.votes
        '''
        
        data_json = json.loads(self.response.read())
        df=pd.DataFrame(data_json)
        N_votes=len(df)
        for n in range(N_votes):
            # # puts votes in the right format, as database returns all strings
            df['power'].iloc[n]=int(df['power'].iloc[n])
            df['balance'].iloc[n]=int(df['balance'].iloc[n])
            df['lockedBalance'].iloc[n]=int(df['lockedBalance'].iloc[n])
        df['createdAt']=df['createdAt'].apply(lambda x:datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))
        df['updatedAt']=df['updatedAt'].apply(lambda x:datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))
                
        
        self.votes=df
    
    def update(self):
        '''
        prints what was the latest vote together with the number of votes casted
        '''
        self.getVotes()
        df=self.votes
        last=df['updatedAt'].max()
        print(' last vote was updated at ')
        print(last)
        print(' as of right now, there have been {} recorded votes'.format(len(df)))
        

        
        
        
        
        
        
    
    
    
    
if __name__=='__main__':
    votes=Votes()

    votes.update()
    vv=votes.votes
            
        
    
