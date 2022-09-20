#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 11:17:06 2022

This module is used to get the relevant data from the 
sentinel database.

Needs: SQLAlchemy and pandas
pip install SQLAlchemy==1.3.7
It also needs a connection string to the sentinel DB, which im storing locally
as a txt file. You'll need to provide this. 

@author: JP, juan.madrigalcianci@protocol.ai
"""

import sqlalchemy as sqa
import pandas as pd


class sentinel:
    """
    class to connect to the sentinel database.
    """

    def __init__(self, connString):
        try:
            self.connection = sqa.create_engine(connString).connect()
            print("connected to sentinel")
        except:
            print("Error while connecting")



    def customQuery(self, SQL):
        # print('performing custom query...')
        df = pd.read_sql(SQL, self.connection)
        # print('done!')
        return df




if __name__ == "__main__":
    import time

    # reads the connection string stored as a text file in
    # SecretString.txt
    f = open("SecretString.txt", "r")
    NAME_DB = f.read()

    # initializes the class
    db = sentinel(NAME_DB)

    # gets derived gas output dataframe
    MIN_BLOCK = 2044500
    t0 = time.time()
    # df=db.getGasfromBlock(minBlock=MIN_BLOCK,unique=False)
    tf = time.time() - t0
    print("request time " + str(tf) + "seconds")
