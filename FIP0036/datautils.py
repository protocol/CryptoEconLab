#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:19:15 2022

@author: juan
"""
# imports required libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sentinel import sentinel




def longFromShort(Id:str,list_of_addresses_and_ids:list):
    '''
    Gets long Id (address) from short ID
    

    Parameters
    ----------
    Id : str
        short id.
    list_of_addresses_and_ids : list
       a list with addresses and ids

    Returns
    -------
    long : str
        address associated with Id

    '''
    
    try:
        long=list_of_addresses_and_ids[
            list_of_addresses_and_ids['id']==Id]['address'].values[0]
    except:
         long=None
    return long
    
def getShortId(signature:dict,list_of_addresses_and_ids:list):
    '''
    gets short id from long-format address

    Parameters
    ----------
    signature :  dict
        dictionary with the signatures we want to get id for
    list_of_addresses_and_ids : list
       table with addresses and Ids

    Returns
    -------
    None.

    '''
    
    
    X=signature['signer']
    try:
        signature['short']=list_of_addresses_and_ids[
            list_of_addresses_and_ids['address']==X
            ]['id'].values[0]
    except:
 
        signature['short']=None
        
    return signature
    
    
  


def addShortAndLongId(signature:dict,list_of_addresses_and_ids:list):
    
    X=signature['signer']
    
    
    if 'f0'==X[:2]:  # checks if starts with f0. If if does, signature is shortformat
        try:
           signature['short']=X
           signature['long']=longFromShort()
           
           
           list_of_addresses_and_ids[
               list_of_addresses_and_ids['id']==X
               ]['address'].values[0]
        except:
            signature['long']=None
               
    else:
        try:
            signature['long']=X
            signature['short']=list_of_addresses_and_ids[
                list_of_addresses_and_ids['address']==X
                ]['id'].values[0]
            
            
        except:
            signature['short']=None
        
    return signature
    
    




def is_in_list(x:str,list_:list):
    '''
    checks if an address x is in the list_
    
    used to check if x is in list_

    Parameters
    ----------
    x : str
        address.
    list_ : list
        list to be checked against

    Returns
    -------
    is_it : boolean
        True if it is, false otherwise
    '''
    

    is_it=x in list_
    return is_it



def connect_to_sentinel(secret_string: str):
    """
    creates a connection coursor to the sentinel database

    Parameters
    ----------
    secret_string : str
        connection string to connect to sentinel. it should have the form:
        postgres://readonly:j<PASSWORD>@read.lilium.sh:13573/mainnet?sslmode=require

    Returns
    -------
    db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel

    """
    f = open(secret_string, "r")
    NAME_DB = f.read()

    # initializes the class
    db = sentinel(NAME_DB)
    return db
def get_miner_locked_funds(database: sentinel, height: int):
    
    
    try:
        miner_locked=pd.read_csv('datasets/miner_locked.csv')
    except:
        print('miner locked balances  not found, querrying sentinel ...')

    
        QUERY = """
        SELECT DISTINCT "miner_id", "height", "pre_commit_deposits", "initial_pledge", "locked_funds"
        FROM "visor"."miner_locked_funds"            
        WHERE "height"<='{}'
        ORDER BY "height" DESC
       """.format(height)
        miner_locked = database.customQuery(QUERY)
        miner_locked.to_csv('datasets/miner_locked_funds.csv')
    return miner_locked
        
    
    

    
    


def get_miner_sector_deals(database: sentinel, miner_id: str, height: int):
    """
    Returns a pandas dataframe with information regarding sector deals for
    miner with `miner_id` updated until `height`

    Parameters
    ----------
    database : sentinel
        db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel
    miner_id : str
        id of the miner we want to get this info from
    height : int
        cutoff height.

    Returns
    -------
    sector_deals : pandas.Dataframe containing relevant data;
    "miner_id","sector_id","activation_epoch","expiration_epoch",
    "deal_weight","verified_deal_weight","height"

    """

    QUERY = """
    SELECT "miner_id","sector_id","activation_epoch","expiration_epoch",
    "deal_weight","verified_deal_weight","height"
    FROM "visor"."miner_sector_infos"            
    WHERE "height"<='{}', miner_id='{}'
    ORDER BY "height" DESC
   """.format(height, miner_id
    )
    sector_deals = database.customQuery(QUERY)
    return sector_deals


def get_owned_SPs(database: sentinel,  height: int):
    """
    Get SP addresses owned by or with worker id `owner_id` up until `height`

    Parameters
    ----------
    database : sentinel
        db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel
    owner_id : str
        owner or worker id we want to do this with
    height : int
        cutoff height.

    Returns
    -------
    miner_infos :  pandas.Dataframe containing relevant data;
    "miner_id", "multi_addresses", "height"
    """

    try:
        miner_infos=pd.read_csv('datasets/miner_infos.csv')
    except:
        print('miner info (owner/worker) not found, querrying sentinel ...')


        QUERY = """
        SELECT "miner_id", "owner_id", "worker_id", "height"
        FROM "visor"."miner_infos"            
        WHERE "height"<='{}'
        ORDER BY "height" DESC
       """.format(height)
        miner_infos = database.customQuery(QUERY)
        miner_infos=miner_infos.sort_values(by='height')
        miner_infos=miner_infos.groupby(by='miner_id').head(1)

        miner_infos.to_csv('datasets/miner_infos.csv')
    return miner_infos


def is_worker_or_owner(Id,list_of_miners):
    ''' checks if the Id corresponds to a worker or an owner, by checking if
        such an Id can be found in the given column'''
    
    worker=Id in list(list_of_miners['worker_id'])
    owner=Id in list(list_of_miners['owner_id'])
    
    if owner==False and worker==True:
        result='worker', 
        otherID=list_of_miners[list_of_miners['worker_id']==Id]['owner_id'].values[0]
    if owner==True:
        result='owner'
        otherID=list_of_miners[list_of_miners['owner_id']==Id]['worker_id'].values[0]
    if owner==False and worker==False:
        result='Neither'
        otherID=None
    return result,otherID

def get_owners_and_workers(data:pd.core.frame.DataFrame,
                           address: str):
    
    
    '''
    returns a list of miner_id that have owner or worker =address
    '''
    
    SPs=[]
    labels=[]
    
    Y_owner=np.array(data[data['owner_id']==address]['miner_id'].unique())
    N_owner=len(Y_owner)
    
    if N_owner>0:
        for yy in Y_owner:
            labels.append('owner')
            SPs.append(yy)
    
    
    
    Y_worker=data[data['worker_id']==address]['miner_id'].unique()
    N_worker=len(Y_worker)
    if N_worker>0:
        
        for yy in Y_worker:
            labels.append('worker')
            SPs.append(yy)

    SPs=pd.DataFrame([SPs,labels]).T
    
    SPs.columns=['miner_id','type']
    
    return SPs['miner_id'].unique()
    
    



def get_all_power_actors(database: sentinel, height: int):
    """
    generates a list of all miners with their power QAP and RBP

    Parameters
    ----------
    database : sentinel
        db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel

    height : int
        cutoff height.

    Returns
    -------
    power_actors : pandas dataframer containing a list of all miners with their power QAP and RBP

    """
    QUERY = """
            SELECT DISTINCT "miner_id", "height", "state_root", "raw_byte_power", "quality_adj_power"
            FROM "visor"."power_actor_claims"            
            WHERE "height"<={}
            ORDER BY "height" DESC
            """.format(height)
    power_actors = database.customQuery(QUERY)
    return power_actors


def get_addresses(database: sentinel,height:int):
    """
    Parameters
    ----------
    database : sentinel
        db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel

    Returns
    -------
    actors : pandas dataframe with list of all different actors
        DESCRIPTION.

    """

    try:
        
        actors=pd.read_csv('datasets/list_of_addresses.csv')
    except:
        print('list of addresses not found, querying...')
        QUERY = """SELECT "id", "address" FROM "visor"."id_addresses"  WHERE height<='{}'
        """.format(height)
        actors = database.customQuery(QUERY)
        actors.to_csv('datasets/list_of_addresses.csv')
    return actors


def get_active_power_actors(database: sentinel, height: int):
    """
    generates a list of all active (with deals expiring after max_height) miners with their power QAP and RBP

    Parameters
    ----------
    database : sentinel
        db : a sentinel object which is essenyially an sql aclhemy cuorsor connected to sentiel

    height : int
        cutoff height.

    Returns
    -------
    power_actors : pandas dataframer containing a list of all active miners with their power QAP and RBP

    """
    try:
        active_powers = pd.read_csv("datasets/power_actors.csv")
    except:
        power_actors = get_all_power_actors(database=database, height=height)
        positive_powers = power_actors[power_actors["quality_adj_power"] > 0]
        active_powers = positive_powers.sort_values(
            "height", ascending=False
        ).drop_duplicates("miner_id")
        active_powers.to_csv("datasets/power_actors.csv")
    return active_powers



def get_power(miner_id:str, list_of_powers:pd.core.frame.DataFrame):
    try:
        power=list_of_powers[list_of_powers['miner_id']==miner_id]['raw_byte_power'].values[0]
    except:
        power=0
    return power



def get_market_deals_from_id(market_deals:pd.core.frame.DataFrame,
                           user_id: str, side:str):
    '''
    return the market deals that involve 'user_id' as eihter a client or a provider

    Parameters
    ----------
    market_deals : pd.core.frame.DataFrame
        DESCRIPTION.
    user_id : str
        DESCRIPTION.
    side : str
        'client_id' or 'provider_id', determines which side we are looking at

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    '''

   
    df=market_deals[market_deals[side]==user_id] 

    return df


def get_market_deals(database: sentinel,  height: int):
    

    
    try:
        deals=pd.read_csv('datasets/market_deals.csv')
    except:
            
        
        print('getting list of market deal proposals...')

        query='''SELECT DISTINCT "piece_cid",  "unpadded_piece_size",
        "client_id", "provider_id","height" 
        FROM "visor"."market_deal_proposals"
        WHERE "height"<={} AND "end_epoch">={} AND "start_epoch"<={}'''.format(height,height,height)
        
        deals= database.customQuery(query)
        deals.to_csv('datasets/market_deals.csv')
        
    return deals


def toObs(group,name:str):
    
    tally=group.tally
    
    total=tally['Approve']+tally['Reject']
    
    
    Approve={"group":name,
    "Approve":tally['Approve'],
    "percent":tally['Approve']/total}
    
    Reject={"group":name,
        "Approve":tally['Reject'],
        "percent":tally['Reject']/total}
    
    return Approve,Reject




def get_balances(database: sentinel,  height: int):
    '''
    
    return a list of balances up-untila centain height
    

    Parameters
    ----------
    database : sentinel
        DESCRIPTION.
    height : int
        DESCRIPTION.

    Returns
    -------
    balances : TYPE
        DESCRIPTION.

    '''
    
    
    try:
        balances=pd.read_csv('datasets/balances.csv')
    except:
                
        
        print('getting list of balances proposals...')

        query='''SELECT DISTINCT "id", "balance", "height"  
        FROM "visor"."actors"
        WHERE "height"<={}'''.format(height)
        
        balances= database.customQuery(query)
        balances.to_csv('datasets/balances.csv')
        
    return balances
    




if __name__ == "__main__":
    minerId = "f01740934"

    HEIGHT = 2162760

    db = connect_to_sentinel(secret_string="SecretString.txt")
    locked=get_miner_locked_funds(database=db, height=HEIGHT)
    
    # msd=get_miner_sector_deals(database=db,miner_id=minerId,height=HEIGHT)
