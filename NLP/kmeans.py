#!/usr/bin/env python
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import pandas as pd
import argparse
import os
import glob
from mysql.connector import connect, Error
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
# Metadata
__program__ = "Pre-Process files to start PICALO"
__author__ = "Britt Vink"
__maintainer__ = "Britt Vink"
__email__ = "bvink@umcg.nl"
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
        self.prefix = getattr(arguments, 'prefix')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'k-meanscluster')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
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
        df = pd.read_pickle("df_topics_kcbbe.pkl")

        # initialize the vectorizer
        vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_df=0.95)
        # fit_transform applies TF-IDF to clean texts - we save the array of vectors in X
        X = vectorizer.fit_transform(df['cleaned'])

        Sum_of_squared_distances = []
        K = range(2, 20)
        for k in K:
            km = KMeans(n_clusters=k, max_iter=200, n_init=20)
            km = km.fit(X)
            Sum_of_squared_distances.append(km.inertia_)
        self.make_ellbowplot(K, Sum_of_squared_distances)

        # initialize kmeans with 3 centroids
        kmeans = KMeans(n_clusters=11, random_state=42)
        # fit the model
        kmeans.fit(X)
        # store cluster labels in a variable
        clusters = kmeans.labels_

        # initialize PCA with X components
        pca = PCA(n_components=11, random_state=42)
        # pass our X to the pc and store the reduced vectors into pca_vecs
        pca_vecs = pca.fit_transform(X.toarray())
        # save our two dimensions into x0 and x1
        x0 = pca_vecs[:, 0]
        x1 = pca_vecs[:, 1]

        df['cluster'] = clusters
        df['x0'] = x0
        df['x1'] = x1

        df.to_pickle("df_kmeans_clustering.pkl")
        self.get_top_keywords(10, clusters, vectorizer, X)
        self.mapcluster_kmeans(df)


    def make_ellbowplot(self, K, Sum_of_squared_distances):
        plt.plot(K, Sum_of_squared_distances, 'bx-')
        plt.xlabel('k')
        plt.ylabel('Sum_of_squared_distances')
        plt.title('Elbow Method For Optimal k')

        outpath = os.path.join(self.outdir,
                               "{}_Ellbowplot.png".format(self.prefix))
        plt.savefig(outpath)
        # plt.show()


    def get_top_keywords(self, n_terms, clusters, vectorizer, X):
        """This function returns the keywords for each centroid of the KMeans"""
        df = pd.DataFrame(X.todense()).groupby(clusters).mean()  # groups the TF-IDF vector by cluster
        terms = vectorizer.get_feature_names_out()  # access tf-idf terms

        outpath = os.path.join(self.outdir,
                               "{}_top_keywords.txt".format(self.prefix))
        f = open(outpath, "w")

        for i, r in df.iterrows():
            f.write('\nCluster {}'.format(i))
            f.write(','.join([terms[t] for t in np.argsort(r)[-n_terms:]]))
            # for each row of the dataframe, find the n terms that have the highest tf idf score
        f.close()


    def mapcluster_kmeans(self, df):
        # map clusters to appropriate labels
        # cluster_map = {0: "sport", 1: "tech", 2: "religion"}
        # # apply mapping
        # df['cluster'] = df['cluster'].map(cluster_map)

        # set image size
        plt.figure(figsize=(12, 7))
        # set a title
        plt.title("TF-IDF + KMeans clustering", fontdict={"fontsize": 18})
        # set axes names
        plt.xlabel("X0", fontdict={"fontsize": 16})
        plt.ylabel("X1", fontdict={"fontsize": 16})
        # create scatter plot with seaborn, where hue is the class used to group the data
        sns.scatterplot(data=df, x='x0', y='x1', hue='cluster', palette="viridis", alpha=0.5)

        # sns.scatterplot(data=df, x='x0', y='x1', hue='cluster', palette="viridis", alpha=0.5)
        outpath = os.path.join(self.outdir,
                               "{}_scatterplot.png".format(self.prefix))
        plt.savefig(outpath)


if __name__ == '__main__':
    m = main()
    m.start()