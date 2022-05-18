#!/usr/bin/env python

from sklearn.cluster import SpectralClustering
import numpy as np
import yake
import matplotlib.pyplot as plt
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from scipy import spatial
import argparse
import pandas as pd
from nltk import word_tokenize, pos_tag
import logging


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
        logging.basicConfig(filename="logfile_spectral_clustering.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        df = pd.read_pickle("df_topics_kcbbe.pkl")

        logging.info("df with shape " + str(df.shape))

        # Take keywords for each post and turn them into a textstring
        sentences = self.extract_keywords(df)
        logging.info("keywords token")

        # Get list keyword sets of all articles
        data_tokenized = [word_tokenize(i) for i in sentences]
        keyword_sets = [set(post) for post in data_tokenized]
        logging.info("keyword sets for all articles is made")

        # Make model
        self.make_model(data_tokenized)
        logging.info("model is made")

        # Get vector for tokenized data
        df_vectors_tokenized_data, doc_embeddings_tokenized_data = self.get_doc_embaddings(df, data_tokenized)
        logging.info("df with vectors of tokenized data is made. df has shape: " + str(df_vectors_tokenized_data.shape))
        print(df_vectors_tokenized_data)

        # Cluster and print topics with tokenized data
        clustering_tokenized_data = SpectralClustering(assign_labels="discretize").fit(df_vectors_tokenized_data)

        df["topic clustering tokenized data"]  = clustering_tokenized_data.labels_

        # Print how many article per topic with tokenized data
        print(pd.Series(clustering_tokenized_data.labels_).value_counts())

        self.make_plot(doc_embeddings_tokenized_data, clustering_tokenized_data, "scatterplotscpectralcluster.png")
        self.make_article_distance_df(df, df_vectors_tokenized_data)

        # Get vector for keywordset data
        df_vectors_keywordset, doc_embeddings_keywordsets = self.get_doc_embaddings(df, keyword_sets)
        print(df_vectors_keywordset)

        # Cluster and print topics for keyword set
        clustering_vector_keywordset = SpectralClustering(assign_labels="discretize").fit(df_vectors_keywordset)
        df["topic clustering keyword set"]  = clustering_vector_keywordset.labels_

        # Print how many article per topic for keywordset
        print(pd.Series(clustering_vector_keywordset.labels_).value_counts())

        self.make_plot(doc_embeddings_keywordsets, clustering_vector_keywordset, "scatterplotscpectralcluster_keyword.png")


    def get_doc_embaddings(self, df, data_tokenized):
        doc_embeddings = np.zeros([df.shape[0], 300])
        for i in range(df.shape[0]):
            embeddings = np.array(self.doc_embed_from_vectors(data_tokenized[i]))
            doc_embeddings[i, :] = embeddings

        df_vectors = pd.DataFrame(doc_embeddings)
        df_vectors.index = df.index.tolist()
        return (df_vectors, doc_embeddings)


    def extract_keywords(self, df):
        # Keyword extractor
        simple_kwextractor = yake.KeywordExtractor()
        sentences = []
        for post in df.cleaned:
            post_keywords = simple_kwextractor.extract_keywords(post)
            sentence_output = ""
            for word, number in post_keywords:
                sentence_output += word + " "

            sentences.append(sentence_output)
        return sentences


    def make_article_distance_df(self, df, df_vectors):
        doc_embeddings = np.zeros([df.shape[0], df.shape[0]])
        for i in range(df_vectors.shape[0]):
            for a in range(df_vectors.shape[0]):
                embeddings = np.array(spatial.distance.cosine(df_vectors.iloc[i], df_vectors.iloc[a]))
                doc_embeddings[i, a] = embeddings

        df_article_distance = pd.DataFrame(doc_embeddings)
        df_article_distance.columns = df.index
        df_article_distance.index = df.index
        df_article_distance.to_pickle("df_article_distance.pkl")


    def make_plot(self, vector_data, cluster, outputname):
        plt.scatter(vector_data[:, 0], vector_data[:, 1], c=cluster.labels_)
        plt.savefig(outputname)


    def vectors_from_posts(self, post):
        all_words = []
        for words in post:
            all_words.append(words)
        return (self.wv[all_words])


    def doc_embed_from_vectors(self, post):
        test_vectors = self.vectors_from_posts(post)
        return test_vectors.mean(axis=0)


    def make_model(self, data_tokenized):
        # demesions for embedding specific word

        model = Word2Vec(sentences=common_texts, vector_size=300, window=5, min_count=1, workers=4)
        model.save("word2vec.model")
        model = Word2Vec.load("word2vec.model")
        model.build_vocab(data_tokenized, update=True)
        # Store just the words + their trained embeddings.
        word_vectors = model.wv
        word_vectors.save("word2vec.wordvectors")
        # Load back with memory-mapping = read-only, shared across processes.
        self.wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')
        # vector = wv['computer']  # Get numpy vector of a word
        # sims = wv.most_similar('computer', topn=10)  # get other similar words


    def print_arguments(self):
        print("Arguments:")
        print("")


if __name__ == '__main__':
    m = main()
    m.start()
