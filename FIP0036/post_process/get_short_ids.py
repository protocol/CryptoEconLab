#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 18:33:59 2022

@author: juan
"""

from tqdm import tqdm
import os




def get_short_addresses_on_chain(long:list):
    '''
    queries lotus directly to get short Ids from long ids
    
    
    REQUIRES A LOTUS DAEMON ON THE BACKGROUND

    Parameters
    ----------
    long : list
        a list of addresses in long format

    Returns
    -------
    results : list
        a list of short ids associated to each long address entry

    '''
    
    
    results={'long':long, 'short':[]}
    
    
    for a in tqdm(long):
        
        cmd='/usr/local/bin/lotus state lookup   '+a
        results['short'].append(os.popen(cmd).read())

        
    return results
        
        
    