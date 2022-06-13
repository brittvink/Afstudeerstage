#!/usr/bin/env python

"""
File:         lda_clustering.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to perform LDA clustering

The number of topics is given with the number_topics argument (-nt).
The number of passes is given with the passes argument (-p).

The clustering is performed and the clusters keywords are saved
"""

import os
import argparse
import pickle
import logging
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess

# Metadata
__program__ = "LDA clustering"
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
        self.nt = getattr(arguments, 'number_topics')
        self.passes = getattr(arguments, 'passes')
        self.prefix = getattr(arguments, 'prefix')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'lda')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
        """
                Creates a argument parser
                :return:  ArgumentParser with number_topics, passes and prefix
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
        """
        Dictionary with id2word is created, with the data
        A Term Document Frequency is created
        Than the LDA models is build.
        The dominant cluster is put in the dataframe for each article

                :return: nothing

        """

        self.print_arguments()

        logging.basicConfig(filename=self.outdir + "/logfile.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("start")

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")

        data_words = df.cleaned.values.tolist()
        data_ready = self.process_words(data_words)

        lda_model, corpus = self.make_lda_model(data_ready)
        self.topic_per_article(df, lda_model, corpus)


    def make_lda_model(self, data_ready):
        """
        LDA model is made, the model and corpus are returned
                :param data_ready: dataframe
                :return: nothing

        """

        # Create Dictionary
        id2word = corpora.Dictionary(data_ready)
        logging.info("dictionary created")

        # Create Corpus: Term Document Frequency
        corpus = [id2word.doc2bow(text) for text in data_ready]
        logging.info("corpus created")

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

        logging.info("model created")


        with open(os.path.join(self.outdir,
                                    "data_{}_topics_{}_passes_topics.txt".format(self.nt, self.passes)), 'w') as f:
            f.writelines(str(lda_model.print_topics()))
        f.close()

        pickle.dump(lda_model, open(os.path.join(self.outdir,
                               "lda_model_{}_topics_{}_passes.pk".format(self.nt, self.passes)), 'wb'))

        pickle.dump(corpus, open(os.path.join(self.outdir,
                                    "corpus_{}_topics_{}_passes.pk".format(self.nt, self.passes)), 'wb'))

        pickle.dump(data_ready, open(os.path.join(self.outdir,
                                      "data_{}_topics_{}_passes.pk".format(self.nt, self.passes)), 'wb'))

        logging.info("Finished LDA")
        return [lda_model, corpus]


    def topic_per_article(self, df, lda_model, corpus):
        """
        The dominant topic of each article is determined. The topic is added to the dataframe

        :param df: Dataframe
        :param lda_model: lda_model
        :param corpus: corpus
        :return: nothing
        """

        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(lda_model[corpus]):
            row = list(row)
            row = sorted(list(row)[0], key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = lda_model.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(
                        pd.Series([int(topic_num), round(prop_topic, 4), topic_keywords]), ignore_index=True)
                else:
                    break

        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
        sent_topics_df.index = df.index

        result = pd.concat([df, sent_topics_df], axis=1)
        result.to_pickle(self.outdir + "/clustered.pkl")


    def process_words(self, texts):
        """
        List of lists is made of a String

                :param texts: String
                :return: nothing

        """

        texts_out = [[word for word in simple_preprocess(str(doc))] for doc in texts]
        return texts_out


    def print_arguments(self):
        """
        Arguments are printed in the terminal
                        :return: nothing

        """
        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()