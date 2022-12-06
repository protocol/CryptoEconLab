#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the utilities module

Created on Sun Dec  4 10:35:40 2022

@author: juan
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




def getPowers(miners:list):
    ''' returns a list of powers, given a list of miners'''
    
    powers=[m.power() for m in miners]        
    return powers



