#!/usr/bin/env python

"""
File:         df_to_csv.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to read a text file and put the data in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""

import string

import pandas as pd

"""This file creates a csv file given a dataframe as .pkl file"""

df = pd.read_pickle("oud/Information_joined.pkl")
print(df)

df.to_csv("artikel_data.csv.zip", compression='zip')