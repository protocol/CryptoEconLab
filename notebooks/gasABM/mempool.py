#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the Mempool class. It stores trx before they get included in the blocks
@author: juan
"""

# Agent class for Mempool


class Mempool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def remove_transaction(self, transaction):
        self.transactions.remove(transaction)

    def remove_transactions(self, transactions):

        [self.transactions.remove(t) for t in transactions]
