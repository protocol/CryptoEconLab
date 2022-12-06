#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:06:26 2022

@author: juan
"""

def createMessage(self,gas:float,
                  gasLimit:float,
                  bid:float,
                  baseFee:float,
                  tip:float,
                  Class:str,
                  sender:str,
                  time:float):
    
    m={'gasUsed':gas,
       'gsLimit':gasLimit,
       'bid':bid,
       'baseFee':baseFee,
       'tip':tip,
       'sender':sender,
       'class':Class,
       'time':time,
       'included':False,
       'profit':min(baseFee+tip,bid)
        }
    
    return m