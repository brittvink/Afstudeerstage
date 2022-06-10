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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'processing')
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
        logging.basicConfig(filename=os.path.join(self.outdir,"logfile_preprocessing.log"),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        df = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        data_tokenized = df.tokenized.tolist()
        keyword_sets = df.keywords.tolist()

        logging.info("colums kokenized and keyword_sets added to the dataframe. Dataframe is saved as df_preprocessed.pkl")

        # Make model
        self.make_model(data_tokenized, keyword_sets)

        logging.info("model made and saved")

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
        doc_embeddings = np.zeros([df.shape[0], 300])
        for i in range(df.shape[0]):
            embeddings = np.array(self.doc_embed_from_vectors(data_tokenized[i]))
            doc_embeddings[i, :] = embeddings

        df_vectors = pd.DataFrame(doc_embeddings)
        df_vectors.index = df.index.tolist()
        return (df_vectors, doc_embeddings)


    def vectors_from_posts(self, post):
        all_words = []
        for words in post:
            all_words.append(words)

        return self.wv[all_words]


    def doc_embed_from_vectors(self, post):
        test_vectors = self.vectors_from_posts(post)
        return test_vectors.mean(axis=0)


    def make_model(self, data_tokenized, keyword_sets):
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


    def make_article_distance_df(self, df, df_vectors, outputname):
        doc_embeddings = np.zeros([df.shape[0], df.shape[0]])
        for i in range(df_vectors.shape[0]):
            for a in range(df_vectors.shape[0]):
                embeddings = np.array(spatial.distance.cosine(df_vectors.iloc[i], df_vectors.iloc[a]))
                doc_embeddings[i, a] = embeddings

        df_article_distance = pd.DataFrame(doc_embeddings)
        df_article_distance.columns = df.index
        df_article_distance.index = df.index
        print(df_article_distance)
        df_article_distance.to_pickle(os.path.join(self.outdir,outputname))


    def print_arguments(self):
        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()