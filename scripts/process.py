"""
File:         process.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to process data

The data is readed and vectorized.
The vectorized data is saved and a similarity matrix of the vectors is made, which is saved as well.
"""

import numpy as np
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from scipy import spatial
import argparse
import pandas as pd
import logging
import pickle
import os

# Metadata
__program__ = "processing"
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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'processing')
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
        A model from where the word2vec vectors come from is made.
        Than the vectors for all articles are determined, by getting the mean of all vectors for all words in the article.
        The dataframe with the vectors is saved.
        Than a similarity matrix is made determining the similarity between articles based on their vectors. This dataframe is saved as well.
        This process is done for both keyword data and cleaned data.

                :return: nothing

        """

        self.print_arguments()
        logging.basicConfig(filename=os.path.join(self.outdir,"logfile_preprocessing.log"),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        data_tokenized = df.tokenized.tolist()
        keyword_sets = df.keywords.tolist()

        # Make model
        self.make_model(data_tokenized, keyword_sets)

        # Get vector for tokenized data
        df_vectors_tokenized_data, doc_embeddings_tokenized_data = self.get_doc_embaddings(df, data_tokenized)

        df_vectors_tokenized_data.to_pickle(os.path.join(self.outdir,"df_vectors_tokenized_data.pkl"))
        pickle.dump(doc_embeddings_tokenized_data, open(os.path.join(self.outdir,"doc_embeddings_tokenized_data.pk"), 'wb'))

        self.make_article_distance_df(df, df_vectors_tokenized_data, "df_article_distance_tokenized_data.pkl")
        logging.info('"df_article_distance_tokenized_data.pkl" is made')

        # Get vector for keywordset data
        df_vectors_keywordset, doc_embeddings_keywordsets = self.get_doc_embaddings(df, keyword_sets)

        df_vectors_keywordset.to_pickle(os.path.join(self.outdir,"df_vectors_keywordset.pkl"))
        pickle.dump(doc_embeddings_keywordsets, open(os.path.join(self.outdir,"doc_embeddings_keywordsets.pk"), 'wb'))

        self.make_article_distance_df(df, df_vectors_keywordset, "df_article_distance_keywords.pkl")
        logging.info('"df_article_distance_keywords.pkl" is made')


    def get_doc_embaddings(self, df, data_tokenized):
        """
        The vector for each row of the dataframe is found using the data_tokenized List.

        :param df: Dataframe
        :param data_tokenized: List
        :return: dataframe and np.array
        """
        doc_embeddings = np.zeros([df.shape[0], 300])
        for i in range(df.shape[0]):
            embeddings = np.array(self.doc_embed_from_vectors(data_tokenized[i]))
            doc_embeddings[i, :] = embeddings

        df_vectors = pd.DataFrame(doc_embeddings)
        df_vectors.index = df.index.tolist()
        return (df_vectors, doc_embeddings)


    def vectors_from_posts(self, post):
        """
        A list of all words is made, than the vectors for all these words is returned.

        :param post: row of dataframe
        :return: vectors of all words
        """

        all_words = []
        for words in post:
            all_words.append(words)

        return self.wv[all_words]


    def doc_embed_from_vectors(self, post):
        """
        The mean of all vectors of a post is returned

        :param post: row of dataframe
        :return: Dataframe
        """
        test_vectors = self.vectors_from_posts(post)
        return test_vectors.mean(axis=0)


    def make_model(self, data_tokenized, keyword_sets):
        """
        A vector model of all words is all the posts is made, and saved.

        :param data_tokenized: List
        :param keyword_sets: List
        :return: nothing
        """

        # demesions for embedding specific word
        model = Word2Vec(sentences=common_texts, size=300, window=5, min_count=1, workers=4)
        model.save(os.path.join(self.outdir,"word2vec.model2"))
        model = Word2Vec.load(os.path.join(self.outdir,"word2vec.model2"))
        model.build_vocab(data_tokenized, update=True)
        model.build_vocab(keyword_sets, update=True)
        # Store just the words + their trained embeddings.
        word_vectors = model.wv
        word_vectors.save(os.path.join(self.outdir,"word2vec.wordvectors2"))
        # Load back with memory-mapping = read-only, shared across processes.
        self.wv = KeyedVectors.load(os.path.join(self.outdir,"word2vec.wordvectors2"), mmap='r')
        logging.info("model made and saved")


    def make_article_distance_df(self, df, df_vectors, outputname):
        """
        For each article the distance with all other articles is calculated. The calculations are saved in a dataframe.

        :param df: Dataframe
        :param df_vectors: Dataframe
        :param outputname: String
        :return: nothing
        """
        doc_embeddings = np.zeros([df.shape[0], df.shape[0]])
        for i in range(df_vectors.shape[0]):
            for a in range(df_vectors.shape[0]):
                embeddings = np.array(spatial.distance.cosine(df_vectors.iloc[i], df_vectors.iloc[a]))
                doc_embeddings[i, a] = embeddings

        df_article_distance = pd.DataFrame(doc_embeddings)
        df_article_distance.columns = df.index
        df_article_distance.index = df.index
        df_article_distance.to_pickle(os.path.join(self.outdir,outputname))


    def print_arguments(self):
        """
        Arguments are printed in the terminal
        :return: nothing
        """

        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()