#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from groups import groups
from tqdm import tqdm
from preprocess import dataPreprocess
from counting import countVote
import pandas as pd
import numpy as np

export_path='../Public_Data'


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
ADD_MSIGS=False
HEIGHT = 2162760
#####################################################################################
#
#               gets relevant datasets
#
####################################################################################
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
print('there are {} different signatures'.format(N_votes))



list_of_addresses_and_ids=datasets['addresses']
list_long_short=datasets['longShort']

ms2=pd.read_json('datasets/ms.json')
ms2['yes']=np.zeros(len(ms2))
ms2['count']=np.zeros(len(ms2))
ms2['no']=np.zeros(len(ms2))
is_msig=[]





#####################################################################################
#
#               main loop
#
####################################################################################

#%%
for ii in tqdm(range(N_votes)):

    vote = list_of_votes.iloc[ii]
    groups_of_voters,signatures,ms2=countVote(vote,groups_of_voters,
                                              datasets,signatures,ms2)


#####################################################################################
#
#               displays tallied votes
#
####################################################################################
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

#####################################################################################
#
#              exports
#
####################################################################################    

def to_dict(vote):
    
    aux={'signer':vote.signer,
        'vote':vote.vote,
        'quantity':vote.quantity,
        'other':vote.other,
        'groupID':vote.groupID,
        'index':vote.index
        }
    return aux


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




all_votes_l=[]
for aa in all_votes:
    for ii in aa:
        all_votes_l.append(ii)

dv=[]

for dd in all_votes_l:
    dv.append(dd.to_dict())
dv=pd.DataFrame(dv)
dv=dv[dv['quantity']>0]
summary=dv.groupby(by=['groupID','vote'])['quantity'].sum()


dg=dv[dv['groupID']!=4]
dg['quantity']=dg['quantity']
dg['groupID']=dg['groupID'].apply(lambda x: str(x))    
dg['quantity']=dg['quantity'].apply(lambda x: float(x))    
dg.to_csv('dg.csv')

dt=dv[dv['groupID']==4]
dt['quantity']=dt['quantity'].apply(lambda x: float(x))    
dt.to_csv('dt.csv')


###############################################################################
#
#              in case we are counting msigs
#
###############################################################################   

if ADD_MSIGS:

    dts=dt
    yesM=ms2[ms2['yes']>=ms2['Threshold']]
    noM=ms2[ms2['no']>=ms2['Threshold']]
    th=groups_of_voters['token']
    i_=len(dt)
    for i in range(len(yesM)):
        
        vote={'signer':yesM['ID'].iloc[i],
              'vote':'Approve', 
              'quantity':yesM['Balance'].iloc[i], 
              'other':'', 
              'groupID':4}
        
        aa=pd.DataFrame(vote,index=[0])
        dtY=pd.concat([dt,aa])
    
    
    for i in range(len(noM)):
        
        vote={'signer':noM['ID'].iloc[i],
              'vote':'Reject', 
              'quantity':noM['Balance'].iloc[i], 
              'other':'', 
              'groupID':4}
        
        aa=pd.DataFrame(vote,index=[])
        dtN=pd.concat([dt,aa])
        
        
    
    
    


    
