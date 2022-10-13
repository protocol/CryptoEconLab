#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 17:03:00 2022
defines classes for each of the groups

Group 1: Deal Storage (weighted by Deal Bytes)
SPs sign the voting message from their owner address or worker address
Group 2: Capacity (weighted by Raw Bytes)
SPs sign the voting message from their owner address or worker address
Group 3: Clients (weighted by Deal Bytes)
Client sign the voting message from their deal making account (the account used to propose deals)  
Group 4: Token Holders (weighted by FIL balance, for both regular wallet and multisig accounts)
Sign the voting message using their wallet account
A multisig wallet vote is valid when the number of signatures received from the token holders(that are signers of the multisig)  matches the threshold
I.e: if a multisig has 5 signers with threshold as 3, then 3 out of 5 signers must sign and submit the voting message.


@author: JP. 
juan.madrigalcianci@protocol.ai
"""
import pandas as pd
from dataclasses import dataclass

@dataclass
class Vote:
    signer:str
    vote:str
    quantity:str
    other:dict
    groupID:int
    index:int
    
    
    def to_dict(self):
        
        aux={'signer':self.signer,
            'vote':self.vote,
            'quantity':self.quantity,
            'other':self.other,
            'groupID':self.groupID,
            'index':self.index
            }
        return aux
        
        

class groups:
    '''
    This is a generic group object. it takes 
    
    * `groupid`, where
    
    1. deal storage
    2. capacity
    3. clients
    4. token holders
    5. core dev    
    
   * `votes` is an array counting the votes (''Aprove, "Reject", "Abstain")
   * `address` address of the person or multisig that voted
   * `quantity` displays the quantity of each vote, it could be, e.g., raw bytes, head count, etc
   * `idType` miner_id or worker_id if groupdid=1 , regular or multisig if groupid=4, else None
    
    
    '''
    def __init__(self,groupID):
        self.groupID=groupID
        self.votedMoreThanOnce=[]
        self.listVotes=[]
        
        names={'1':'deals',
               '2':'capacity',
               '3': 'clients',
               '4':'token_holder',
               '5':'core_dev'}
        
        self.groupName=names[str(self.groupID)]
    
    
    def validateAndAddVote(self,signature:dict,amount=None,other_info:dict=[],validate=True):
        '''
        validates and adds a vote (as a dict) as a new vote on this group.
        Notice that an address might be able to vote for two different groups
        but not fo the same group more than once

        Parameters
        ----------
        signature : dict
            a dictionary with the signature information

        '''
        
        
        # gets right vote quantity 
        
        if self.groupID==1 or self.groupID==2 or self.groupID==3:
            quantity=int(signature['power'])
        elif self.groupID==4:

            quantity=int(signature['balance'])

                
        elif self.groupID==5:
            quantity=1
        else: 
            print('wrong group ID!')
        
            
        
        if validate and self.is_ellegible(signature["address"]):
            
        
            if amount is not None:
                quantity=amount
                
            thisVote=Vote(signer=signature["address"],
                        vote=signature["optionName"],
                        quantity=quantity,
                        other=other_info,
                        groupID=self.groupID,
                        index=len(self.listVotes))
                
                
            self.listVotes.append(thisVote)


        else:
             self.votedMoreThanOnce.append(signature["address"])
    
             
    
    def list_to_df(self):
        
        df=[]
        for ll in self.listVotes:
            df.append(ll.to_dict() )
        return pd.DataFrame(df)
        
        
        
        
        
        
        
    
            
    
    def removeVote(self,address):
        '''
        removes a vote with address \addresss\. This is useful when overriding stuff

        Parameters
        ----------
        address : str
            signer address of the vote to remove
        '''
        for vv in self.listVotes:
            if vv.signer==address:
                self.listVotes.remove(vv)
        
    
    
    
    def has_voted(self,address:str):
        has_voted=False
        for vv in self.listVotes:
            if address==vv.signer:
                has_voted=True
        return has_voted
        
        
    def is_ellegible(self,address:str):
        '''
        checks whether an address `address` is ellegible (i.e., hasnt it already voted)        

        Parameters
        ----------
        adress:: str
            address

        Returns
        -------
        is_it : boolean
            `is_it` ellegible? True or False, 

        '''
        
        is_it=True
        for vv in self.listVotes:
            if address==vv.signer:
                is_it=False
    
        return is_it
    
    def getUnits(self):
        '''
        gets the units for each voting category; can be bytes, people or tokens

        Returns
        -------
        units : str
            units for the groupID

        '''
        Id=self.groupID
        if Id==1 or Id==2 or Id==3:
            units='PiB'
        elif Id==4:
            units=' FIL'
        elif Id==5:
            units=' devs'
        else:
            print('wrong group ID!')
        return units
        
        
        
    def count(self):
        '''
        tallies the votes stored in the group.

        Returns
        -------
        

        '''
        list_of_votes=pd.DataFrame(self.listVotes)
        total_votes=list_of_votes['quantity'].sum()
        print('-----------')
        
        if  self.groupID==1 or self.groupID==2 or self.groupID==3:
            divisor=2**50
        elif self.groupID==4:
            divisor=int(1e18)
        else:
            divisor=1

        self.tally = list_of_votes.groupby("vote")["quantity"].sum().to_dict()
        total_votes = sum(self.tally.values())/divisor
        for op, voted_for_op in self.tally.items():
            voted_for_op=voted_for_op/divisor
            

            
            
            print('option: '+str(op))
            print('There were a total of '+str(voted_for_op)+' '+self.getUnits()+' in favor of '+op)
            print('this represents {}% of the vote'.format(round(100*voted_for_op/(total_votes),6) ))
            print('-----------')

             

# if __name__=='__main__':
    
#     OUTCOMES=['Approve','Reject','Abstain']
#     GROUPS=['deals','capacity','clients','tokens','devs']
#     N_VOTES=100
#     deals=groups(1)
#     capacity=groups(2)
#     clients=groups(3)
#     tokens=groups(4)
#     devs=groups(5)
    
#     voters={
#         "deals":deals,
#         "capacity":capacity,
#         "clients":clients,
#         "tokens":tokens,
#         "devs":devs}


    
#     for i in range(N_VOTES):
#         for gr in GROUPS:
#             vote=np.random.choice(OUTCOMES)
#             address='f2_sample_'+str(i)+'_'+gr
#             if gr=='tokens':
#                 quantity=np.random.randint(int(1e18))
#             elif gr=='deals' or gr=='clients' or gr=='capacity':
#                 quantity=np.random.randint(int(1e15),int(1e17))
#             else:
#                 quantity=1

#             voters[gr].votes.append(vote)
#             voters[gr].address.append(address)
#             voters[gr].quantity.append(quantity)

# #Tests the tallying of the votes#
#     for gr in GROUPS:
#         print('###################')
#         print('Counting '+str(gr))
#         print('###################')
#         print('')
#         print('')
        
#         voters[gr].count()
        
        print('')
    
        
        
        
        
        
        





        
        

        
        