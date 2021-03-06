#!/usr/bin/env python

"""
File:         NMF.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to perform NMF

The clustering is performed and the clusters keywords are saved
"""

import pickle
import pandas as pd
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import argparse


# Metadata
__program__ = "NMF clustering"
__author__ = "Britt Vink"
__maintainer__ = "Britt Vink"
__email__ = "b.vink@st.hanze.nl"
__license__ = "GPLv3"
__version__ = 1.0
__description__ = "{} is a program developed and maintained by {}. " \
                  "This program is licensed under the {} license and is " \
                  "provided 'as-is' without any warranty or indemnification " \
                  "of any kind.".format(__program__,
                                        __author__,
                                        __license__)


class main():
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'NMF')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
        """
                Creates a argument parser
                :return:  ArgumentParser
                """
        parser = argparse.ArgumentParser(prog=__program__,
                                         description=__description__,
                                         )
        # Add optional arguments.
        parser.add_argument("-v",
                            "--version",
                            action="version",
                            version="{} {}".format(__program__,
                                                   __version__),
                            help="show program's version number and exit.")

        return parser.parse_args()


    def start(self):
        """
        Tfidf Vectors are made. Than the model is made and the model is fitted to the TF-IDF.
        Than all keywords of the clusters are printed and the clusters for each article are saved in a dataframe.

        :return: nothing
        """

        documents = pd.read_pickle("pre_processing/df_preprocessed.pkl")

        vect = TfidfVectorizer()
        # Fit and transform
        X = vect.fit_transform(documents.cleaned)

        # Create an NMF instance: model
        model = NMF(n_components=11, random_state=5)
        # Fit the model to TF-IDF
        model.fit(X)

        # Transform the TF-IDF: nmf_features
        nmf_features = model.transform(X)
        pickle.dump(model, open(self.outdir + "/NMFmodel.pk", 'wb'))

        # Create a DataFrame: components_df
        components_df = pd.DataFrame(model.components_, columns=vect.get_feature_names())

        for topic in range(components_df.shape[0]):
            tmp = components_df.iloc[topic]
            print(f'For topic {topic + 1} the words with the highest value are:')
            print(tmp.nlargest(10))
            print('\n')

        df = pd.DataFrame(nmf_features).idxmax(axis=1)
        df.index = documents.index

        documents = documents.merge(df.to_frame(), left_index=True, right_index=True)
        documents.to_pickle("NMF.pkl")


if __name__ == '__main__':
    m = main()
    m.start()

