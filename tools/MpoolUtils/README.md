# README

######   author: Juan P. Madrigal-Cianci, CEL. 2022.
######         juan.madrigalcianci@protocol.ai   
    
---

This is a tool to get info from the Mpool using glif. It contains the file 
`MpoolUtils.py` which contains two functions:
    
   *  `MpoolQuerry`:    queries the Mpool and saves/attaches to a json file 

   * `listenMpool`:     keeps running MpoolQuerry every "freq" seconds until
                     it quits. i.e., it keeps gathering data
 
See relevant docstrings in the script. The file `test.py` provides a minimally working example of how to use the `MpoolQuerry` method to grab gas data from the Mpool and plots it.


This is in the hopes that it might be useful to estimate demand, as well as
for visualizing messages that do not necessarilly get included on the chain.
    



