#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the miner class. Since in Filecoin miners are also user,
this class inherits from the user class
"""
import numpy as np
from user import User
from transaction import Transaction
from constants import MAX_GAS_LIMIT
from survival import survival


class Miner(User):
    
    def __init__(self, user_id:str, balance:float, power:float,
                 packStrategy:callable,demandProfile:callable):
        '''
        

        Parameters
        ----------
        user_id : str
            a string identifying this user
        balance : float
            how many tokens do they have
        power : float
           a number between 0 and 1, denoting the relative power of this miner
           in the network
        packStrategy : callable
            A strategy for how to pack messages/trx in blocks. it takes a list of
            trx and returns a a list sorted in order of inclusion preference and gamma, 
            a number between 0 and 1 denoting the proportion of block to be used for incl
            (ex: gamma=1, tries to fill the whole block)
        demandProfile : callable
            a funciton that determines how many trx to send for a given base fee

        Returns
        -------
        None.

        '''
        super().__init__(user_id, balance,demandProfile)
        self.miner_id = user_id
        self.blocks_mined = 0
        self.power = power
        self.packStrategy=packStrategy
        self.demandProfile=demandProfile


    def select_transactions(self, mempool, base_fees):
        '''
        selects which trx to include in a block; this happens when
        this miner gets chosen to mine

        Parameters
        ----------
        mempool : Mempool object
            the mempool
        base_fees : Tfloat
            the current base fee

        Returns
        -------
        block_transactions :list of transaction types
           
        block_fee : float
            the total amount of token burnt by this inclusion
        block_gas_used : float
            how much gas was used by that inclusion

        '''
       # Initialize block
        block_transactions = []
        block_gas_used = 0
        block_fee = 0
        base_fee=base_fees[-1]
        # sorts and decides how much to pack        
        gamma,transactions=self.packStrategy(mempool, base_fees)
    
        for transaction in transactions:

            if block_gas_used + transaction.gas_limit <= MAX_GAS_LIMIT * gamma:
                block_transactions.append(transaction)
                block_gas_used += transaction.gas_limit
                block_fee += transaction.get_fee(base_fee)
            else:
                break
        
        return block_transactions, block_fee, block_gas_used


