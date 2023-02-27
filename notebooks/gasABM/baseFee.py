#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an auxiliary module used to compute base fees

@author: juan
"""
from constants import TARGET_GAS, MIN_BASE_FEE


def BaseFee(gasUtilisation:float, currentBaseFee:float,c:float=1/8):
    '''
    computes the current EIP 1559 basefee with an update parameter of c=1/8

    Parameters
    ----------
    gasUtilisation : float
        how much gas was used at a given block
    currentBaseFee : float
        base fee at current block
    c: float
        step-size in the eip-1559 update

    Returns
    -------
    base fee: float
        base fee updated.

    '''
    
    bf = currentBaseFee * \
        (1 + 0.125 * (gasUtilisation - TARGET_GAS) / TARGET_GAS)
    return max(bf, MIN_BASE_FEE)
