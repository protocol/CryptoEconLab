#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 23:27:17 2022

@author: juan
"""

import json
import datautils as utils

def countVote(vote,groups_of_voters,datasets,signatures):

    list_of_deals=datasets['deals']
    list_of_miners=datasets['miners']
    list_of_addresses_and_ids=datasets['addresses']
    list_of_core_devs=datasets['core']
    list_of_powers=datasets['powers']
    list_long_short=datasets['longShort']
    list_of_balances=datasets['balances']


    
    signature=json.loads(vote["signature"])
    X = signature["signer"]
    signature=utils.addShortAndLongId(signature=signature,
                list_of_addresses_and_ids=list_of_addresses_and_ids,
                longShort=list_long_short)
    #
    # checks if it;s a core dev and adds headcount
    #
    is_core_dev =utils.is_in_list(X, list_of_core_devs)
    
    
    
    if is_core_dev:
        groups_of_voters["core"].validateAndAddVote(signature)
    
    #
    # checks if exists and adds balance
    #
    #exists = utils.is_in_list(X, list_of_addresses)
    #if exists:
    if vote['balance']>0:
        groups_of_voters["token"].validateAndAddVote(signature)
    #
    # Iterate over all deals, adding up the bytes of deals where X is the proposer (client)
    #  
    dealsForX=utils.get_market_deals_from_id(list_of_deals,
                                             user_id=signature['short'],
                                             side='client_id') 
    #print('length {}'.format(len(dealsForX)))
    totalBytes = dealsForX["padded_piece_size"].sum()
    # checks that address X has not voted and has >0 bytes as a client
    if totalBytes > 0:
        groups_of_voters["client"].validateAndAddVote(signature,amount=totalBytes)
    #
    # Iterate over all SPs, checking if X is the owner / worker of an SP Y
    #
    
    signature['client_bytes']=totalBytes
    
    # checks if this is an owner account, and overwrites worker account vote if it is,
    #or if its a worker account and owner has already voted, stops counting
    #--------------------------------------------------------------------------
    #checks if signature['short'] corresponds to an owner or worker id
    result,otherID=utils.is_worker_or_owner(Id=signature['short'],
                                            list_of_miners=list_of_miners)
    
    # if it's a wallet or miner account, skips it, in the first case because it doesnt have miners
    # in the second one because they get accounted for with the owner/worker address
    if result=='Neither':
        signatures.append(signature)
        #print('account address')
        return groups_of_voters,signatures

    
    
 
    
    #if it's an owner, override the entries from the worker, if they exist
    
    if otherID!=signature['short']:
    
        otherID_long=utils.longFromShort(otherID, list_of_addresses_and_ids)
        has_other_voted=(groups_of_voters['capacity'].has_voted(otherID_long)) or (groups_of_voters['deal'].has_voted(otherID_long))
    
    
    
        if result=='owner' and has_other_voted:
            print(' ')
            print('overwritting '+otherID_long)
            #gets the other ID in long format
            #if otherID_long is in the address that alread voted, remove
            for gr in ['capacity','deal']:
                
                if has_other_voted and (otherID_long!=signature['signer']):
    
                    groups_of_voters[gr].removeVote(otherID_long)
            
        # and if its a worker and owner has already votes, skip            
        elif result=='worker' and  has_other_voted:
    
            print(' ')
            print('{} had already voted, skipping'.format(otherID_long))
            signatures.append(signature)
    
            return groups_of_voters,signatures
            
            
    
    
            
    #--------------------------------------------------------------------------

    SPs= utils.get_owners_and_workers(list_of_miners,signature['short'])
    
    # #
    # Add Y's raw bytes to the SP capacity vote (Group 2)
    #
    total_power_SPs=0
    totalBytesY=0
    
    
    other_info={'miner_ids':[]}
    for Y_i in SPs:
 
        power_Y_i=utils.get_power(Y_i, list_of_powers)
        #if power_Y_i.size>0:
        total_power_SPs+=power_Y_i
        #
        # Iterate over all deals, adding up the bytes of deals
        # where Y is the provider, add these bytes to Deal Storage vote (Group 1)
        #
        dealsByY=utils.get_market_deals_from_id(list_of_deals,
                                                 user_id=Y_i,
                                                 side='provider_id')
    
        totalBytesY += dealsByY["padded_piece_size"].sum()
        #
        # from Add Y's raw bytes to the SP capacity vote (Group 2)
        #
        other_info['miner_ids'].append(Y_i)
        #
        # Adds miner balance, if any 
        #
        # balance_yi=list_of_balances[list_of_balances['minerId']==Y_i]
        # if len(balance_yi)>0:
        #     av_balance_yi=int(balance_yi['balance'].values[0])-int(balance_yi['lockedBalance'].values[0])
        #     groups_of_voters["token"].validateAndAddVote(signature,amount=av_balance_yi,validate=False)
                
        
        
        
        
    groups_of_voters["capacity"].validateAndAddVote(signature,amount=total_power_SPs,other_info=other_info)
    groups_of_voters["deal"].validateAndAddVote(signature,amount=totalBytesY)
    
    signature['capcity_bytes']=total_power_SPs
    signature['deal_bytes']=totalBytesY
    vote_out=signature['capcity_bytes']+signature['deal_bytes']+signature['client_bytes']

    signature['diff']=int(signature['power'])-vote_out
    signatures.append(signature)
    # import pdb
    # pdb.set_trace()
    
    return groups_of_voters,signatures
    