#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the transaction module.
It creates a transaction object
@author: juan
"""


class Transaction:
    def __init__(self, gas_limit:float, tip:float, sender_id:str):
        '''
        
        This creates a trx object. This is what users and miners submit to
        the Mpool and chain

        Parameters
        ----------
        gas_limit : float
            gas limit of the trx
        tip : float
            miner tip.
        sender_id : str
            id of the sender; examples: miner, user, 0001).

        Returns
        -------
        None.

        '''
        self.gas_limit = gas_limit
        self.tip = tip
        self.sender_id = sender_id

    def get_fee(self, base_fee:float)->float:
        '''
        Returns the fee, in tokens, associated to the trx

        Parameters
        ----------
        base_fee : float
            current base fee.

        Returns
        -------
        float
            how much a user pays of the the base fee.

        '''
        return base_fee * self.gas_limit
