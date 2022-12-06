#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:52:16 2022

@author: juan
"""

class lane:
    '''
    This is the lane class. It introduces a gas lane object, that has a 
    maximum block size ::size::, a target block size ::target:: an initial base fee
    ::initial_base_fee:: and a base fee updatring mechanism, basefee function. 
    
    
    '''
    def __init__(self,size:float,
                 target:float,
                 initial_base_fee:float,
                 base_fee_function:callable,
                 name:str=''):
        
        self.size=size
        self.target=target
        self.base_fee=initial_base_fee
        self.base_fee_function=base_fee_function
        
    def update_basefee(self,G:float):
        self.base_fee=self.base_fee_function(G,self.base_fee,self.target)
        


class Block:
    '''
    This is the block class. It takes a list of lanes. 
    '''
    
    
    def __init__(self,inputLaneParams,basefee):
        
        
        N=len(inputLaneParams)
        self.lanes=[]
        for i in range(N):
            self.lanes.append(lane)
            
    # def update_basefee
        
        
        
        
            
            


        


if __name__=='__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    bf = lambda x,b,T: b*(1+0.125*(x-T)/T+(0.125*(x-T)/T)**2/2)
    bf = lambda x,b,T: b*(1+0.125*(x-T)/T)

    k=np.log(9/8)
    #bf = lambda x,b,T: b*np.exp(k*(x-T)/T)

    
    SIZE=10E9
    target=SIZE/2
    B0=1
    N=1000
    M=1000
    Prices=[]
    for m in range(M):
    
        ell=lane(SIZE,target,B0,bf)

    
        price=[]
        price.append(B0)
        for i in range(N):
            G=SIZE*np.random.random()
            ell.update_basefee(G)
            price.append(ell.base_fee)
        plt.plot(price,color='LightGray',alpha=0.4)
        Prices.append(price)
    plt.plot(np.mean(Prices,0),color='k')
        
    