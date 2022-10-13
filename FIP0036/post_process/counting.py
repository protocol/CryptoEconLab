#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 23:27:17 2022

@author: juan
"""

import json
import datautils as utils



def findMsigs(signature,ms2):
    
    '''returns list of multisigs that have ::signature:: as a signer '''
    
    
    signer=signature['short']
    
    
    msig_ids=[]
    
    for i in range(len(ms2)):
        vv=ms2['Signer'].iloc[i]
        if signer in vv:
            print('count')

            msig_ids.append(ms2['ID'].iloc[i])
            ms2['count'].iloc[i]+=1
            
     
            
            if ms2['yes'].iloc[i] < ms2['Threshold'].iloc[i] and ms2['no'].iloc[i] < ms2['Threshold'].iloc[i]:
            
                if signature['optionName']=='Approve':
                    ms2['yes'].iloc[i]+=1
                elif signature['optionName']=='Reject':
                    ms2['no'].iloc[i]+=1
                
       
    return ms2,msig_ids




def countVote(vote,groups_of_voters,datasets,signatures,ms2):

    list_of_deals=datasets['deals']
    list_of_miners=datasets['miners']
    list_of_addresses_and_ids=datasets['addresses']
    list_of_powers=datasets['powers']
    list_long_short=datasets['longShort']
    list_of_balances=datasets['balances']

    
    

    #--------------------------------------------------------------------------
    #
    # Prepares the vote: gets some info related to the vote
    #
    #--------------------------------------------------------------------------
    signature=json.loads(vote["signature"])
    
    # This is a fix originated from having manually addded core dev votes into the filPOll
    
    if signature=={}:
        signature['signer']=vote['signerAddress']
        signature['address']=vote['address']

        signature['constituentGroupId']=vote['constituentGroupId']
        signature['balance']=0
        signature['power']=0
        if vote['optionId']==50:
            signature['optionName']='Reject'
        elif vote['optionId']==49:
            signature['optionName']='Approve'
        
    
    # adds short id to the vote. This is necesary for the table lookup
    signature=utils.addShortAndLongId(signature=signature,
                list_of_addresses_and_ids=list_of_addresses_and_ids,
                longShort=list_long_short)
    
    
    
    
    is_msig= signature['short'] in list(ms2['ID'])
        

    ms2,msig_ids=findMsigs(signature,ms2)  
    signature['msigs']=msig_ids
    
    if is_msig:
        signature['is_msig']=True
    else:
        signature['is_msig']=False


        
    

    
    
    #checks if it's a core dev by chcecking if constituent group =6.
    # this value was hardcoded by filpoll
    is_core_dev =vote['constituentGroupId']==6 

    # check if its an owner or worker address
    result,otherID=utils.is_worker_or_owner(Id=signature['short'],
                                        list_of_miners=list_of_miners)
    
    
    # see which SPs have signature as owner or worker
    SPs= utils.get_owners_and_workers(list_of_miners,signature['short'])
    
    #--------------------------------------------------------------------------
    #
    #  votes as core dev
    #
    #--------------------------------------------------------------------------
     
    if is_core_dev:
        groups_of_voters["core"].validateAndAddVote(signature)
    
    #--------------------------------------------------------------------------
    #
    # votes as token holder
    #
    #--------------------------------------------------------------------------
    if vote['balance']>0:
        groups_of_voters["token"].validateAndAddVote(signature)
    #--------------------------------------------------------------------------
    #
    # votes as client; Iterate over deals, adds bytes where X is the proposer
    #
    #--------------------------------------------------------------------------        

    dealsForX=utils.get_market_deals_from_id(list_of_deals,
                                             user_id=signature['short'],
                                             side='client_id') 
    totalBytes = dealsForX["padded_piece_size"].sum()
    if totalBytes > 0:
        groups_of_voters["client"].validateAndAddVote(signature,
                                                      amount=totalBytes)
    
    #--------------------------------------------------------------------------
    #
    # checks for overriding SP votes
    #
    #--------------------------------------------------------------------------        
    result,otherID=utils.is_worker_or_owner(Id=signature['short'],
                                            list_of_miners=list_of_miners)

    
    if otherID!=signature['short']:
    
        otherID_long=utils.longFromShort(otherID, list_of_addresses_and_ids)
        has_cap_voted=groups_of_voters['capacity'].has_voted(otherID_long) 
        has_deal_voted= groups_of_voters['deal'].has_voted(otherID_long)
        has_other_voted=has_cap_voted or has_deal_voted
    
        #if it's an owner, override the entries from the worker, if they exist    
        if result=='owner' and has_other_voted:
            print(' ')
            print('overwritting '+otherID_long)
            for gr in ['capacity','deal']:   
                if has_other_voted and (otherID_long!=signature['signer']):
                    groups_of_voters[gr].removeVote(otherID_long)
            
        # and if its a worker and owner has already votes, skip            
        elif result=='worker' and  has_other_voted:
            print(' ')
            print('{} had already voted, skipping'.format(otherID_long))
            signatures.append(signature)
            return groups_of_voters,signatures,ms2

    #--------------------------------------------------------------------------
    #
    # Adds up SP votes (commited capacity and deal SPs)
    #
    #--------------------------------------------------------------------------
    
    total_power_SPs=0
    totalBytesY=0
    other_info={'miner_ids':[]}    
    
    for Y_i in SPs:
        power_Y_i=utils.get_power(Y_i, list_of_powers)
        total_power_SPs+=power_Y_i
        #--------------------------------------------------------------------------
        #
        # Iterate over all deals, adding up the bytes of deals
        # where Y is the provider, add these bytes to Deal Storage vote (Group 1)
        #
        #--------------------------------------------------------------------------
        dealsByY=utils.get_market_deals_from_id(list_of_deals,
                                                 user_id=Y_i,
                                                 side='provider_id')
        #adds each SPs RBP to the total bytes counter
        totalBytesY += dealsByY["padded_piece_size"].sum()
        #--------------------------------------------------------------------------
        #
        # from Add Y's raw bytes to the SP capacity vote (Group 2)
        #
        #--------------------------------------------------------------------------
        other_info['miner_ids'].append(Y_i)
        #
        # Adds miner Available balance (balance-locked-pledged), if any 
        #
        balance_yi=list_of_balances[list_of_balances['minerId']==Y_i]
        if len(balance_yi)>0:
            av_balance_yi=int(balance_yi['balance'].values[0])
            av_balance_yi+=-int(balance_yi['lockedBalance'].values[0])
            av_balance_yi+=-int(balance_yi['initial_pledge'].values[0])
            groups_of_voters["token"].validateAndAddVote(signature,
                                                         amount=av_balance_yi,
                                                         validate=False)
    
    


                   
    groups_of_voters["capacity"].validateAndAddVote(signature,
                                                    amount=total_power_SPs,
                                                    other_info=other_info)
    groups_of_voters["deal"].validateAndAddVote(signature,amount=totalBytesY)
    
    
    #updates signature tracker
    signature['client_bytes']=totalBytes
    signature['capcity_bytes']=total_power_SPs
    signature['deal_bytes']=totalBytesY
    vote_out=totalBytes+total_power_SPs+totalBytesY
    
    signature['diff']=int(signature['power'])-vote_out
    signatures.append(signature)

    
    return groups_of_voters,signatures,ms2
    