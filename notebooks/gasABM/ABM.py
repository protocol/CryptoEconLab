#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main loop for the gas ABM 
@author: juan
"""

import numpy as np
from baseFee import BaseFee
import matplotlib.pyplot as plt
from tqdm import tqdm
from constants import MAX_MEMPOOL_SIZE
from chain import Chain


def ABM(params,verbose:bool=False,plots:bool=True):
    '''
    

    Parameters
    ----------
    params : dict
        a dictionary with the required parameters, namely:
            
            -miners, a list of miners
            -users, a list of users
            -mempool: a mempool object
            -power: A list with the powers of each miner
            -num blocks: simulation length
            - base fee: initial base fee
            -R block reward function
            
            
            
            .
    verbose : bool, optional
        if we want to print output states at every steps. The default is False.
    plot : bool, optional
        if we want to plot at the end. The default is True.

    Returns
    -------
    res : dict
        a dictionary containing observable quantities; 

    '''
    miners=params['miners']
    users=params['users']
    mempool=params['mempool']
    power=params['power']
    numBlocks=params['numBlocks']
    base_fee=params['basefee']
    R=params['R']
    
    base_fee_history = [base_fee]
    mpoolSize=np.zeros(numBlocks)
    gu=np.zeros(numBlocks)
    # starts main loop
    
    
    chain=Chain()
    
    for i in tqdm(range(numBlocks)):
        # Collect stats

        num_transactions = 0
        ############################################################
        #
        #
        # creates miner trx
        #
        #
        ############################################################
        for miner in miners:
            transactionsM = miner.create_transactions(base_fee, miner=True)
            for transaction in transactionsM:
                mempool.add_transaction(transaction)
            num_transactions += len(transactionsM)
        # adds users trx
        
        ############################################################
        #
        #
        # creates user trx
        #
        #
        ############################################################
        for user in users:
            transactionsU = user.create_transactions(base_fee, miner=False)
            for transaction in transactionsU:
                mempool.add_transaction(transaction)
            num_transactions += len(transactionsU)
    
        ############################################################
        #
        #
        # puts a restriction on max mpool size
        #
        #
        ############################################################
        if len(mempool.transactions) > MAX_MEMPOOL_SIZE:
            mempool.transactions = mempool.transactions[-MAX_MEMPOOL_SIZE:]
    
        ############################################################
        #
        #
        # chooses a miner according to their power and makes it mine a blocl
        #
        #
        ############################################################
        # packs Trx in block.
        miner = np.random.choice(miners, size=1, p=power)[0]
        block_transactions, block_fee, block_gas_used = miner.select_transactions(
            mempool, base_fee_history)
        miner.balance += R
        ############################################################
        #
        #
        # includes trxs on chain, and removes from mempool
        #
        #
        ############################################################    
        chain.update(transactions=block_transactions,
                     epoch=i, basefee=base_fee, used=block_gas_used, 
                     burnt=block_fee)
        mempool.remove_transactions(block_transactions)
        mpoolSize[i]=len(mempool.transactions)
        gu[i] = block_gas_used
        # Update base fee
        base_fee = BaseFee(block_gas_used, base_fee_history[-1])
        base_fee_history.append(base_fee)
    
        # Print stats
    
        if verbose:
    
            print("Block ", i)
            print("Base Fee: ", base_fee)
            print("Mempool Size: ", len(mempool.transactions))
            print("block size: ", len(block_transactions))
            print('new messages ', num_transactions)


    res={'miners':miners,
            'users':users,
            'mempool':mempool,
            'power':power,
            'numBlocks':numBlocks,
            'basefee':base_fee_history,
            'R':R,
            'gasUsed':gu,
            'mpoolSize':mpoolSize,
            'chain':chain}

    if plots:

        plt.plot(base_fee_history)
        plt.yscale('log')
        plt.xlabel('epoch')
        
        plt.show()
        
        plt.plot(gu)
        plt.title('gas used')
        plt.xlabel('epoch')
        plt.show()
        
        plt.plot(mpoolSize)
        plt.title('mpool size')
        plt.xlabel('epoch')
        plt.show()


    plt.hist(gu)    
    return res
