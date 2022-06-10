#!/usr/bin/env python

import os
import argparse
import pandas as pd
import pickle
import gensim
from gensim.utils import  simple_preprocess
import gensim.corpora as corpora
import logging

import re
import numpy as np
import pandas as pd
from pprint import pprint

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy for lemmatization
import spacy




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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'lda')
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

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")

        data_words = df.cleaned.values.tolist()
        print(data_words)

        data_ready = self.process_words(data_words)  # processed Text Data!
        print(data_ready)

        self.make_lda_model(data_ready, df)


    def make_lda_model(self, data_ready, df):
        logging.basicConfig(filename=self.outdir + "/logfile.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("start")

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


        outpath_data = os.path.join(self.outdir,
                                    "data_{}_topics_{}_passes_topics.txt".format(self.nt, self.passes))

        with open(outpath_data, 'w') as f:
            f.writelines(str(lda_model.print_topics()))
        f.close()

        print(lda_model.print_topics())

        outpath_lda_model = os.path.join(self.outdir,
                               "lda_model_{}_topics_{}_passes.pk".format(self.nt, self.passes))

        pickle.dump(lda_model, open(outpath_lda_model, 'wb'))

        outpath_corpus = os.path.join(self.outdir,
                                    "corpus_{}_topics_{}_passes.pk".format(self.nt, self.passes))

        pickle.dump(corpus, open(outpath_corpus, 'wb'))

        outpath_data = os.path.join(self.outdir,
                                      "data_{}_topics_{}_passes.pk".format(self.nt, self.passes))
        pickle.dump(data_ready, open(outpath_data, 'wb'))

        logging.info("Finished")


        # corpus_transformed = lda_model[corpus]
        # print(corpus_transformed)
        # print(list(zip([a for [(a,b)] in corpus_transformed], data_ready.index())))
        # exit()


        # Init output
        sent_topics_df = pd.DataFrame()

        # Get main topic in each document
        for i, row in enumerate(lda_model[corpus]):
            print(type(row))
            print("\n")
            row = list(row)


            for i in row:
                print(i)
            # row = row.sort()
            # print(row)
            # exit()
            # row = sorted(list(row))
            print(row)
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
        print(result)
        result.to_pickle(self.outdir + "/clustered.pkl")









        # # Add original text to the end of the output
        # contents = pd.Series(texts)
        # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        # return (sent_topics_df)

        # from gensim.test.utils import common_texts, common_corpus, common_dictionary
        # # Init output
        # sent_topics_df = pd.DataFrame()
        #
        # # Get main topic in each document
        # for i, row in enumerate(lda_model[corpus]):
        #     row = sorted(row, key=lambda x: (x[1]), reverse=True)
        #     # Get the Dominant topic, Perc Contribution and Keywords for each document
        #     for j, (topic_num, prop_topic) in enumerate(row):
        #         # we use range here to iterate over the n parameter
        #         if j in range(1):  # => dominant topic
        #             wp = lda_model.show_topic(topic_num)
        #             topic_keywords = ", ".join([word for word, prop in wp])
        #             sent_topics_df = sent_topics_df.append(
        #                 # and also use the i value here to get the document label
        #                 pd.Series([int(i), int(topic_num), round(prop_topic, 4), topic_keywords]),
        #                 ignore_index=True,
        #             )
        #         else:
        #             break
        # sent_topics_df.columns = ["Document", "Dominant_Topic", "Perc_Contribution", "Topic_Keywords"]
        #
        # # Add original text to the end of the output
        # text_col = [common_texts[int(i)] for i in sent_topics_df.Document.tolist()]
        # contents = pd.Series(text_col, name='original_texts')
        # sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        # sent_topics_df



    def process_words(self, texts):
        texts_out = [[word for word in simple_preprocess(str(doc))] for doc in texts]
        return texts_out


    def print_arguments(self):
        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()