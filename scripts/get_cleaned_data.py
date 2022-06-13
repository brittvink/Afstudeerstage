#!/usr/bin/env python

"""
File:         get_cleaned_data.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to clean data.

The data is given with the input argument (-i).
The data is readed, cleand and put in a dataframe
"""


import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
import logging
import argparse
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import os


# Metadata
__program__ = "Clean data"
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
        self.input = getattr(arguments, 'input')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'cleaned_data')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
        """
        Creates a argument parser
        :return:  ArgumentParser with input
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

        parser.add_argument("-i",
                            "--input",
                            default="/Users/brittvink/Desktop/Afstudeerstage/NLP/data/Information_joined.pkl",
                            type=str,
                            help="The path to the input directory.")

        return parser.parse_args()

    def start(self):
        """
        The input data is used as a dataframe.
        A document-term matrix is created using CountVectroizer, and this is saved.
        Than the data is cleaned, and the dataframe is saved

        :param input: String
        :return: nothing
        """

        self.print_arguments()

        df = pd.read_pickle(self.input)

        logging.basicConfig(filename=os.path.join(self.outdir,"logfile_get_cleaned_data.log"),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        # Logging
        logging.info("df: " + str(df.shape) + "with columns" + df.columns)
        logging.info("Column text has an avarage length of: " + str(df["text"].str.len().mean()))
        logging.info("Column text has " + str(df["text"].str.len().sum()) + " words")
        logging.info("Column text has quantiles " + str(df["text"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
        logging.info("Column text has minimal " + str(df["text"].str.len().min()) + " words")
        logging.info("Column text has maximal " + str(df["text"].str.len().max()) + " words")
        logging.info("Data is collected from multiple rssfeeds " + str(df.rss.value_counts()))


        # We are going to create a document-term matrix using CountVectorizer
        cv = CountVectorizer()
        data_cv = cv.fit_transform(df.text)
        data_dtm = pd.DataFrame(data_cv.toarray(),
                                columns=cv.get_feature_names())
        data_dtm.index = df.index

        data_dtm.to_pickle(os.path.join(self.outdir,"data_dtm.pkl"))
        pickle.dump(cv, open(os.path.join(self.outdir,"cv_dtm.pkl"), "wb"))

        # Clean data
        df['cleaned'] = df['text'].apply(lambda x: self.preprocess_text(x, remove_stopwords=True))
        df.to_pickle(os.path.join(self.outdir,"df_cleaned.pkl"))

        # Logging
        logging.info("df: " + str(df.shape) + "with columns" + df.columns)
        logging.info("Column cleaned has an avarage length of: " + str(df["cleaned"].str.len().mean()))
        logging.info("Column cleaned has " + str(df["cleaned"].str.len().sum()) + " words")
        logging.info(
            "Column cleaned has quantiles " + str(df["cleaned"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
        logging.info("Column cleaned has minimal " + str(df["cleaned"].str.len().min()) + " words")
        logging.info("Column cleaned has maximal " + str(df["cleaned"].str.len().max()) + " words")
        logging.info("Stopwords that were removed were: " + str(stopwords.words("english")))


    def preprocess_text(self, text: str, remove_stopwords: bool) -> str:
        """
        This utility function sanitizes a string by:
        - removing links
        - removing special characters
        - removing numbers
        - removing stopwords
        - transforming in lowercase
        - removing excessive whitespaces

        :param text: String
        :param remove_stopwords: Boolean
        :return: String
        """

        # remove links
        text = re.sub(r"http\S+", "", text)
        # remove special chars and numbers
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)

        # remove stopwords
        if remove_stopwords:
            # 1. tokenize
            tokens = nltk.word_tokenize(text)
            # 2. check if stopword
            tokens = [w for w in tokens if not w.lower() in stopwords.words("english")]
            # 3. join back together
            text = " ".join(tokens)
        # return text in lower case and stripped of whitespaces
        text = text.lower().strip()
        return text


    def print_arguments(self):
        """
        Arguments are printed in the terminal
        :return: nothing
        """
        print("Arguments:")
        print("  > Input : {}".format(self.input))
        print("")


if __name__ == '__main__':
    m = main()
    m.start()