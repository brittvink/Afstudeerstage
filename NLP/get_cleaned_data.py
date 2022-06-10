#!/usr/bin/env python
import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
import logging
import argparse
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
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
        self.input = getattr(arguments, 'input')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'cleaned_data')
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
        parser.add_argument("-i",
                            "--input",
                            default="/Users/brittvink/Desktop/Afstudeerstage/NLP/data/Information_joined.pkl",
                            type=str,
                            help="The path to the input directory.")

        return parser.parse_args()

    def start(self):
        self.print_arguments()

        df = pd.read_pickle(self.input)

        logging.basicConfig(filename=os.path.join(self.outdir,"logfile_get_cleaned_data.log"),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("df: " + str(df.shape) + "with columns" + df.columns)
        logging.info("Column text has an avarage length of: " + str(df["text"].str.len().mean()))
        logging.info("Column text has " + str(df["text"].str.len().sum()) + " words")
        logging.info("Column text has quantiles " + str(df["text"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
        logging.info("Column text has minimal " + str(df["text"].str.len().min()) + " words")
        logging.info("Column text has maximal " + str(df["text"].str.len().max()) + " words")
        logging.info("Data is collected from multiple rssfeeds " + str(df.rss.value_counts()))


        # We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
        cv = CountVectorizer()
        data_cv = cv.fit_transform(df.text)
        data_dtm = pd.DataFrame(data_cv.toarray(),
                                columns=cv.get_feature_names())
        data_dtm.index = df.index

        data_dtm.to_pickle(os.path.join(self.outdir,"data_dtm.pkl"))
        pickle.dump(cv, open(os.path.join(self.outdir,"cv_dtm.pkl"), "wb"))

        data = pd.read_pickle(os.path.join(self.outdir, "data_dtm.pkl"))
        data = data.transpose()

        top_dict = {}
        for c in data.columns:
            top = data[c].sort_values(ascending=False).head(30)
            top_dict[c] = list(zip(top.index, top.values))

        words = []
        for article in data.columns:
            top = [word for (word, count) in top_dict[article]]
            for t in top:
                words.append(t)

        self.identify_common_word(data, words)

        df['cleaned'] = df['text'].apply(lambda x: self.preprocess_text(x, remove_stopwords=True))

        logging.info("df: " + str(df.shape) + "with columns" + df.columns)
        logging.info("Column cleaned has an avarage length of: " + str(df["cleaned"].str.len().mean()))
        logging.info("Column cleaned has " + str(df["cleaned"].str.len().sum()) + " words")
        logging.info(
            "Column cleaned has quantiles " + str(df["cleaned"].str.len().quantile([0.25, 0.5, 0.75])) + " words")
        logging.info("Column cleaned has minimal " + str(df["cleaned"].str.len().min()) + " words")
        logging.info("Column cleaned has maximal " + str(df["cleaned"].str.len().max()) + " words")
        logging.info("Stopwords that were removed were: " + str(stopwords.words("english")))

        # We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
        cv = CountVectorizer()
        data_cv = cv.fit_transform(df.cleaned)
        data_dtm = pd.DataFrame(data_cv.toarray(),
                                columns=cv.get_feature_names())
        data_dtm.index = df.index

        data_dtm.to_pickle(os.path.join(self.outdir,"data_dtm.pkl"))
        pickle.dump(cv, open(os.path.join(self.outdir,"cv_dtm.pkl"), "wb"))

        data = pd.read_pickle(os.path.join(self.outdir,"data_dtm.pkl"))
        data = data.transpose()

        top_dict = {}
        for c in data.columns:
            top = data[c].sort_values(ascending=False).head(30)
            top_dict[c] = list(zip(top.index, top.values))

        words = []
        for article in data.columns:
            top = [word for (word, count) in top_dict[article]]
            for t in top:
                words.append(t)

        self.identify_common_word(data, words)


        df.to_pickle(os.path.join(self.outdir,"df_cleaned.pkl"))



    def identify_common_word(self, data, words):
        # Let's aggregate this list and identify the most common words along with how many routines they occur in
        wordslist = Counter(words).most_common()

        print(wordslist[:10])


    def preprocess_text(self, text: str, remove_stopwords: bool) -> str:
        """This utility function sanitizes a string by:
        - removing links
        - removing special characters
        - removing numbers
        - removing stopwords
        - transforming in lowercase
        - removing excessive whitespaces
        Args:
            text (str): the input text you want to clean
            remove_stopwords (bool): whether or not to remove stopwords
        Returns:
            str: the cleaned text
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
        print("Arguments:")
        print("  > Input : {}".format(self.input))

        print("")

if __name__ == '__main__':
    m = main()
    m.start()