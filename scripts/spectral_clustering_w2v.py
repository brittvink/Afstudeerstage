#!/usr/bin/env python

"""
File:         spectral_clustering_w2v.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to perform spectral clustering

The clustering is performed and the clusters keywords are saved
"""

from sklearn.cluster import SpectralClustering
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import argparse
import pandas as pd
import logging
import pickle
import os


# Metadata
__program__ = "Spectral clustering on Word2Vec vectorized data"
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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'spectral_clustering/word2vec')
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
        Spectral clustering is performed on an array of vectors.
        The keywords for the clusters are saved in a text file.
        A dataframe with the cluster for each article is also saved.

        :return: nothing

        """

        self.print_arguments()
        logging.basicConfig(filename=self.outdir + "/logfile_spectral_clustering.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")

        logging.info("df with shape " + str(df.shape))

        df_vectors_tokenized_data = pd.read_pickle("processing/df_vectors_tokenized_data.pkl")
        # Cluster and print topics with tokenized data
        clustering_tokenized_data = SpectralClustering(assign_labels="discretize").fit(df_vectors_tokenized_data)

        vectorizer = TfidfVectorizer()
        vectorizer.fit_transform(df['cleaned'])

        self.get_top_keywords(10, clustering_tokenized_data.labels_, vectorizer, df_vectors_tokenized_data)

        df["topic clustering tokenized data"]  = clustering_tokenized_data.labels_
        df.to_pickle("spectral_clustering_tdidf.pkl")


    def get_top_keywords(self, n_terms, clusters, vectorizer, X):
        """
        This function returns the keywords for each centroid of the KMeans and writes this to a file.

        :return: nothing
        :param n_terms: Interger
        :param clusters: List
        :param vectorizer: Vectorizer
        :param X: dataframe
        """

        # groups the TF-IDF vector by cluster
        df = pd.DataFrame(X.groupby(clusters).mean())
        # access tf-idf terms
        terms = vectorizer.get_feature_names_out()

        f = open(os.path.join(self.outdir,
                               "top_keywords.txt"), "w")

        for i, r in df.iterrows():
            f.write('\nCluster {}'.format(i))
            f.write(','.join([terms[t] for t in np.argsort(r)[-n_terms:]]))
        f.close()


    def print_arguments(self):
        """
        Arguments are printed in the terminal
        :return: nothing
        """

        print("Arguments:")
        print("")


if __name__ == '__main__':
    m = main()
    m.start()
