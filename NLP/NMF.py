#!/usr/bin/env python

import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

documents = pd.read_pickle("df_topics_kcbbe.pkl")
print(documents.head())

# use tfidf by removing tokens that don't appear in at least 50 documents
vect = TfidfVectorizer()

# Fit and transform
X = vect.fit_transform(documents.cleaned)

# Create an NMF instance: model
# the 10 components will be the topics
model = NMF(n_components=10, random_state=5)

# Fit the model to TF-IDF
model.fit(X)

# Transform the TF-IDF: nmf_features
nmf_features = model.transform(X)

# Create a DataFrame: components_df
components_df = pd.DataFrame(model.components_, columns=vect.get_feature_names())
print(components_df)

for topic in range(components_df.shape[0]):
    tmp = components_df.iloc[topic]
    print(f'For topic {topic+1} the words with the highest value are:')
    print(tmp.nlargest(10))
    print('\n')

print(pd.DataFrame(nmf_features).loc[1].idxmax())
print(pd.DataFrame(nmf_features).idxmax(axis=1).value_counts())