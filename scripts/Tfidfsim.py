#!/usr/bin/env python

"""
File:         Tfidfsim.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to vectorize text data using TF-IDF

The data is readed, vectorized and saved. The similarity between the articles is calculated and saved as well
"""

import logging
import pandas as pd
import argparse
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances


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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'TF-IDF')
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
        The article is described by a vector using the TfidfVectorizer libray.The dataframe with the vectors is saved.
        Than a similairy matrix is made determining the similarity between articles based on their vectors. This dataframe is saved as well.
        This process is done for both keyword data and cleaned data.

        :return: nothing
        """

        logging.basicConfig(filename=self.outdir + "/logfile.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        documents = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        documents["keywords_string"] = [' '.join(map(str, l)) for l in documents['keywords']]

        # use tfidf by removing tokens that don't appear in at least 50 documents
        vect = TfidfVectorizer()
        # Fit and transform
        X = vect.fit_transform(documents.cleaned)

        df = pd.DataFrame(pairwise_distances(X))
        df.index = documents.index.tolist()
        df.columns = documents.index.tolist()
        df.to_pickle(os.path.join(self.outdir,"tf-idf_cleaned_text.pkl"))

        X = vect.fit_transform(documents.keywords_string)

        df = pd.DataFrame(pairwise_distances(X))
        df.index = documents.index.tolist()
        df.columns = documents.index.tolist()
        df.to_pickle(os.path.join(self.outdir, "tf-idf_keywords.pkl"))


if __name__ == '__main__':
    m = main()
    m.start()