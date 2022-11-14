#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code implements a non-homogeneous Poisson process via Poisson thinning
c.f. Boierkens et al, "Handbook of Monte Carlo methods"


Created on Mon Nov 14 11:00:31 2022

@author: Juan P. Madrigal-Cianci, juan.madrigalcianci@protocol.ai
"""

import numpy as np

def nhpp(T:float,
         lam:callable,
         LAM:callable,
         v:float=0.)->np.array:
    '''
    This function is used to generte a Poisson process on a time interval 
    [0,T]. 

    Parameters
    ----------
    T : float
        length of the simulation.
    lam : callable
        rate function, (t,v)|-> lam(t,v).
    LAM : callable
        Upper bound on the rate function, v|->LAM(v)
    v : float
        An auxiliary parameter for the rates
        

    Returns
    -------
    array of points in time that follow a Poisson distr. 

    '''
    
    T = 50;
    
    t=0
    n=0
    times=[t]
    while t<T:
        U=np.random.random()
        Up=np.random.random()
        t=t-np.log(U)/LAM(v)
        if Up< lam(t,v)/LAM(v):
            times.append(t)
            n+=1
    return np.array(times)



if __name__=='__main__':
    import matplotlib.pyplot as plt
    import matplotlib
    font = {'family' : 'serif',
        'size'   : 22}

    matplotlib.rc('font', **font)
    T=50
    lam=lambda t,v: np.sin(t)*np.sin(t)
    LAM=lambda v: 1
    v=0
    
    times=nhpp(T,lam,LAM,v)
    n=np.arange(len(times))
    N=len(n)
    plt.subplots(1,2,figsize=(16,9))
    plt.subplot(121)
    for i in range(N-1):
        plt.plot([times[i],times[i+1]],[n[i],n[i]], color='C0')
        plt.xlabel('time')
        plt.ylabel('Number of arrivals')
        plt.title('Poisson process')
    tt=np.linspace(0,T,100)
    plt.subplot(122)
    plt.plot(tt,lam(tt,v))
    plt.title('$\lambda(t,v)=\sin^2(t)$')
    plt.xlabel('time')
    plt.ylabel('$\lambda(t,v)$')
    plt.tight_layout()

    