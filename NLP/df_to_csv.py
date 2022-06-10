#!/usr/bin/env python
import string

import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer


df = pd.read_pickle("oud/Information_joined.pkl")
print(df)

df.to_csv("artikel_data.csv.zip", compression='zip')
