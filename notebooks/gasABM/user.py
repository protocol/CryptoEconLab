#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 14:57:43 2023

@author: juan
"""
import numpy as np
from constants import DEMAND_FACTOR, INITIAL_BASE_FEE, MAX_GAS_LIMIT
from transaction import Transaction
from survival import survival


# Agent class for users
class User:
    def __init__(self, user_id, balance,demandFunction):
        self.user_id = user_id
        self.balance = balance
        self.demandFunction=demandFunction
        
    def create_transactions(self, base_fee, miner, distr=None):
        
        demandFunction=self.demandFunction
        
        
        bs = 5.7e-9 / 2
        num_transactions=self.demandFunction.getNumberOfMessages(base_fee)

        transactions = []

        for n in range(num_transactions):

            gas_limit = self.demandFunction.getTrxGas(base_fee)
            tip=self.demandFunction.TipDistr()
            self.balance -= gas_limit * base_fee
            transactions.append(Transaction(gas_limit, tip, self.user_id))
        return transactions
