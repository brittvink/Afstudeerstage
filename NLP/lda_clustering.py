#!/usr/bin/env python
import string

import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path
from sklearn.feature_extraction.text import CountVectorizer


import re
import argparse
import pandas as pd
import pickle
import gensim
from nltk.corpus import stopwords
from gensim.utils import  simple_preprocess
import spacy
import gensim.corpora as corpora
import matplotlib.pyplot as plt


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
        self.nt = getattr(arguments, 'number_topics')
        self.passes = getattr(arguments, 'passes')
        self.prefix = getattr(arguments, 'prefix')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'models')
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
        parser.add_argument("-nt",
                            "--number_topics",
                            type=int,
                            required=True,
                            help="How many topics")

        parser.add_argument("-p",
                            "--passes",
                            type=int,
                            required=True,
                            help="How many passes")

        parser.add_argument("-pre",
                            "--prefix",
                            type=str,
                            required=True,
                            help="Prefix for the output file.")


        return parser.parse_args()


    def start(self):
        self.print_arguments()

        df = pd.read_pickle("df_topics_kcbbe.pkl")

        data_words = df.cleaned.values.tolist()
        print(data_words)

        data_ready = self.process_words(data_words)  # processed Text Data!
        print(data_ready)

        self.make_lda_model(data_ready)


    def make_lda_model(self, data_ready):
        # Create Dictionary
        id2word = corpora.Dictionary(data_ready)

        # Create Corpus: Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in data_ready]

        # Build LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                    id2word=id2word,
                                                    num_topics=self.nt,
                                                    random_state=100,
                                                    update_every=1,
                                                    chunksize=10,
                                                    passes=self.passes,
                                                    alpha='symmetric',
                                                    iterations=2,
                                                    per_word_topics=True)

        print(lda_model.print_topics())

        outpath_lda_model = os.path.join(self.outdir,
                               "{}_lda_model_{}_topics_{}_passes.pk".format(self.prefix, self.nt, self.passes))

        with open(outpath_lda_model, 'wb') as pickle_file:
            pickle.dump(lda_model, pickle_file)

        outpath_corpus = os.path.join(self.outdir,
                                         "{}_corpus_{}_topics_{}_passes.pk".format(self.prefix, self.nt, self.passes))
        with open(outpath_corpus, 'wb') as pickle_file:
            pickle.dump(corpus, pickle_file)

        outpath_data = os.path.join(self.outdir,
                                      "{}_data_{}_topics_{}_passes.pk".format(self.prefix, self.nt, self.passes))
        with open(outpath_data, 'wb') as pickle_file:
            pickle.dump(data_ready, pickle_file)


    def process_words(self, texts):
        texts_out = [[word for word in simple_preprocess(str(doc))] for doc in texts]
        return texts_out


    def print_arguments(self):
        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()