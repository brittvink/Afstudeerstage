#!/usr/bin/env python

"""
File:         kmeans_w2v.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to perform kmeans clustering of TF-IDF vectorized data

The clustering is performed and the clusters keywords are saved
"""

import logging
from sklearn.feature_extraction.text import TfidfVectorizer
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import argparse
import os
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import SilhouetteVisualizer


# Metadata
__program__ = "k-means clustering on Word2vec vectorized data"
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
    """ Een nieuwe class"""
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()
        self.prefix = getattr(arguments, 'prefix')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'k-meanscluster/word2vec')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
        """
                Creates a argument parser
                :return:  ArgumentParser with prefix
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

        parser.add_argument("-p",
                            "--prefix",
                            type=str,
                            required=True,
                            help="Prefix for the output file.")

        return parser.parse_args()


    def start(self):
        """
        Data is reade.
        An ellbow plot is made and saved, which can be used to determine the number of clusters.
        K-means clustring is done and the cluster keywords are saved in a textfile.
        For each article the corresponding cluster is added to the dataframe, this dataframe is saved.

                        :return: nothing

        """

        logging.basicConfig(filename=self.outdir + "/{}_logfile.log".format(self.prefix),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("prefix: " + self.prefix)
        logging.info("outdir: " + self.outdir)

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        logging.info("Read in dataframe with the shape: " + str(df.shape))

        # initialize the vectorizer
        vectorizer = TfidfVectorizer()
        logging.info("vectore is initialized")
        # fit_transform applies TF-IDF to clean texts - we save the array of vectors in X
        vectorizer.fit_transform(df['cleaned'])

        X = pd.read_pickle("processing/df_article_distance_keywords.pkl")
        logging.info("fit_transform applied TF-IDF to the cleaned texts")

        Sum_of_squared_distances = []
        K = range(2, 20)
        for k in K:
            km = KMeans(n_clusters=k, max_iter=200, n_init=20)
            km = km.fit(X)
            Sum_of_squared_distances.append(km.inertia_)
        self.make_ellbowplot(K, Sum_of_squared_distances)
        logging.info("ellbowplot made")

        # initialize kmeans with 3 centroids
        kmeans = KMeans(n_clusters=11, random_state=42)
        # fit the model
        kmeans.fit(X)
        logging.info("model is fitted")

        # Calculate Silhoutte Score
        score = silhouette_score(X, kmeans.labels_, metric='euclidean')
        print('Silhouetter Score: %.3f' % score)

        df['cluster'] = kmeans.labels_
        df.to_pickle(self.outdir + "/df_kmeans_clustering.pkl")
        logging.info("clustered information is saved in dataframe with the shape: " + str(df.shape))

        self.get_top_keywords(10, kmeans.labels_, vectorizer, X)
        logging.info("top keywords of topic are written to file")


    def make_ellbowplot(self, K, Sum_of_squared_distances):
        """
        A lineplot is made using the datapoint from the two lists. The plot is saved.
        :param K: List
        :param Sum_of_squared_distances: List
                        :return: nothing

        """
        plt.plot(K, Sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum_of_squared_distances')
        plt.title('Elbow Method For Optimal k')

        outpath = os.path.join(self.outdir,
                               "Ellbowplot.png")
        plt.savefig(outpath)


    def get_top_keywords(self, n_terms, clusters, vectorizer, X):
        """
        This function returns the keywords for each centroid of the KMeans and writes this to a file.

        :param n_terms: Interger
        :param clusters: List
        :param vectorizer: Vectorizer
        :param X: dataframe
        :return: nothing
        """

        df = pd.DataFrame(X.groupby(clusters).mean())  # groups the TF-IDF vector by cluster
        terms = vectorizer.get_feature_names_out()  # access tf-idf terms

        outpath = os.path.join(self.outdir,
                               "top_keywords.txt")
        f = open(outpath, "w")

        for i, r in df.iterrows():
            f.write('\nCluster {}'.format(i))
            f.write(','.join([terms[t] for t in np.argsort(r)[-n_terms:]]))
            # for each row of the dataframe, find the n terms that have the highest tf idf score
        f.close()


if __name__ == '__main__':
    m = main()
    m.start()
