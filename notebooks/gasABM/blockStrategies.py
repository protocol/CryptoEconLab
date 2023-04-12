#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 10:17:59 2023

@author: juan
"""
import numpy as np

def GreedyPack(mempool,basefees):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)


        # Add transactions to block until it's full or there are no more
        # transactions

 
        gamma=1
        return gamma,transactions


def feeAversePack(mempool,basefees,limit=1e-8):
        
    
    gamma=0
    transactions = sorted(
        mempool.transactions,
        key=lambda t: t.tip,
        reverse=True)
    
    if transactions is None:
        transactions=[]
    if basefees[-1]<limit:
# Sort transactions by marginal revenue per unit of gas limit



    # Add transactions to block until it's full or there are no more
    # transactions

 
        gamma=1

    return gamma,transactions


    
def underPack(mempool,basefees):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)


        # Add transactions to block until it's full or there are no more
        # transactions

 
        gamma=1/2
        return gamma,transactions
            
def DeltaPrice(mempool,basefees,factor=5):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)

        # Add transactions to block until it's full or there are no more
        # transactions
        if len(basefees)>factor+1:
            aux=(1*(np.diff(basefees)[-(factor+1):]>0)).mean()
            gamma=1-aux
        else:
            gamma=1

        return gamma,transactions
    
    
def half(mempool,basefees):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)

        # Add transactions to block until it's full or there are no more
        # transactions
        if np.random.random()<0.5:
            gamma=0.5
        else:
            gamma=1

        return gamma,transactions

def semiGreedy(mempool,basefees,lp=0.04,up=0.04):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)

        # Add transactions to block until it's full or there are no more
        # transactions

        u=np.random.random()
        if u<lp:
            gamma=0
        elif u>1-up:
            gamma=1
        else:
            gamma=1
        return gamma,transactions
    
def random(mempool,basefees):
        # Sort transactions by marginal revenue per unit of gas limit
        transactions = sorted(
            mempool.transactions,
            key=lambda t: t.tip,
            reverse=True)

        # Add transactions to block until it's full or there are no more
        # transactions

        gamma=np.random.random()
        return gamma,transactions

    
