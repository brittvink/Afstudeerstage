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

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'spectral_clustering/tf-idf')
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

        return parser.parse_args()


    def start(self):
        self.print_arguments()
        logging.basicConfig(filename=self.outdir + "/logfile_spectral_clustering.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        logging.info("Read in dataframe with the shape: " + str(df.shape))

        # initialize the vectorizer
        vectorizer = TfidfVectorizer()
        logging.info("vectore is initialized")
        # fit_transform applies TF-IDF to clean texts - we save the array of vectors in X
        X = vectorizer.fit_transform(df['cleaned'])
        logging.info("fit_transform applied TF-IDF to the cleaned texts")

        clustering = SpectralClustering(assign_labels="discretize").fit(X)
        self.get_top_keywords(10, clustering.labels_, vectorizer, X)

        df["topic clustering tokenized data"]  = clustering.labels_

        # Print how many article per topic with tokenized data
        print(pd.Series(clustering.labels_).value_counts())

        with (open("processing/doc_embeddings_tokenized_data.pk", "rb")) as openfile:
            doc_embeddings_tokenized_data = pickle.load(openfile)

        self.make_plot(doc_embeddings_tokenized_data, clustering, self.outdir + "/scatterplotscpectralcluster.png")


    def get_top_keywords(self, n_terms, clusters, vectorizer, X):
        """This function returns the keywords for each centroid of the KMeans"""
        df = pd.DataFrame(X.todense()).groupby(clusters).mean()  # groups the TF-IDF vector by cluster
        terms = vectorizer.get_feature_names_out()  # access tf-idf terms

        outpath = os.path.join(self.outdir,
                               "top_keywords.txt")
        f = open(outpath, "w")

        for i, r in df.iterrows():
            f.write('\nCluster {}'.format(i))
            f.write(','.join([terms[t] for t in np.argsort(r)[-n_terms:]]))
            # for each row of the dataframe, find the n terms that have the highest tf idf score
        f.close()


    def make_plot(self, vector_data, cluster, outputname):
        plt.scatter(vector_data[:, 0], vector_data[:, 1], c=cluster.labels_)
        plt.title("Scatterplot of spectral clustering")
        plt.savefig(outputname)


    def print_arguments(self):
        print("Arguments:")
        print("")


if __name__ == '__main__':
    m = main()
    m.start()
