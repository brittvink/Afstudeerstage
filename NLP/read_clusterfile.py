#!/usr/bin/env python

from sklearn.cluster import SpectralClustering
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import logging
import pickle
import os
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_pickle("pre_processing/df_preprocessed.pkl")
# df["len text"] = df['text'].apply(len)
print(df.columns)
df['liststring'] = [', '.join(map(str, l)) for l in df['keywords']]
print(df)


# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
cv = CountVectorizer()
data_cv = cv.fit_transform(df.liststring)
data_dtm = pd.DataFrame(data_cv.toarray(),
                        columns=cv.get_feature_names())
data_dtm.index = df.index
print(data_dtm)

data = data_dtm

data = data.T
# print(data)
# print(type(data))
# data = pd.DataFrame(data.toarray())


top_dict = {}
for c in data.columns:
    top = data[c].sort_values(ascending=False).head(30)
    top_dict[c] = list(zip(top.index, top.values))

words = []
for article in data.columns:
    top = [word for (word, count) in top_dict[article]]
    for t in top:
        words.append(t)

def identify_common_word(data, words):
    # Let's aggregate this list and identify the most common words along with how many routines they occur in
    wordslist = Counter(words).most_common()
    print(wordslist[:10])

identify_common_word(data, words)



# print(df['len text'].max())
# df = pd.read_pickle("data/Information_joined.pkl")
# df = df.groupby(['rss']).count()
