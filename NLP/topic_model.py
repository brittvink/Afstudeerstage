#!/usr/bin/env python

import argparse
import pandas as pd
from nltk import word_tokenize, pos_tag
from gensim import matutils, models
import scipy.sparse
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import CountVectorizer
import pickle


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

        data = pd.read_pickle("data_dtm.pkl")
        cv = pickle.load(open("cv_dtm.pkl", "rb"))
        data_clean = pd.read_pickle("data_clean.pkl")

        tdm = data.transpose()

        # Create a new document-term matrix using only nouns
        # Re-add the additional stop words since we are recreating the document-term matrix
        add_stop_words = ['like', 'im', 'know', 'just', 'dont', 'thats', 'right', 'people',
                          'youre', 'got', 'gonna', 'time', 'think', 'yeah', 'said']
        self.stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)

        corpus, id2word = self.gensim(tdm, cv)
        corpusn, id2wordn = self.dtm_only_nouns(data_clean)
        corpusna, id2wordna, data_dtmna = self.dtm_only_nouns_and_adj(data_clean)

        self.regular_model(corpus, id2word)
        self.nounsonly(corpusn, id2wordn)
        ldana = self.nouns_and_adj(corpusna, id2wordna)

        self.list_topic_per_article(ldana, corpusna, data_dtmna)


    def write_model_to_file(self, model, filename):
        f = open(filename, "w")
        for model in model.print_topics():
            f.write("topic: " + str(model[0]))
            f.write("\n")
            f.write(model[1])
            f.write("\n\n")
        f.close()


    def gensim(self, tdm, cv):
        # We're going to put the term-document matrix into a new gensim format, from df --> sparse matrix --> gensim corpus
        sparse_counts = scipy.sparse.csr_matrix(tdm)
        corpus = matutils.Sparse2Corpus(sparse_counts)

        # Gensim also requires dictionary of the all terms and their respective location in the term-document matrix
        id2word = dict((v, k) for k, v in cv.vocabulary_.items())

        return [corpus, id2word]


    def dtm_only_nouns(self, data_clean):
        # Apply the nouns function to the transcripts to filter only on nouns
        data_nouns = pd.DataFrame(data_clean.text.apply(self.nouns))

        cvn, data_dtmn = self.recreate_dtm(data_nouns)
        corpusn, id2wordn = self.create_gensim_and_vd(cvn, data_dtmn)

        return [corpusn, id2wordn]


    def dtm_only_nouns_and_adj(self, data_clean):
        # Apply the nouns function to the transcripts to filter only on nouns
        data_nouns_adj = pd.DataFrame(data_clean.text.apply(self.nouns_adj))

        cvna, data_dtmna = self.recreate_dtm(data_nouns_adj)
        corpusna, id2wordna = self.create_gensim_and_vd(cvna, data_dtmna)

        return [corpusna, id2wordna, data_dtmna]


    def recreate_dtm(self, data_nouns):
        # Recreate a document-term matrix with only nouns
        cvn = CountVectorizer(stop_words=self.stop_words)
        data_cvn = cvn.fit_transform(data_nouns.text)
        data_dtmn = pd.DataFrame(data_cvn.toarray(), columns=cvn.get_feature_names())
        data_dtmn.index = data_nouns.index

        return [cvn, data_dtmn]


    def create_gensim_and_vd(self, cvn, data_dtmn):
        # Create the gensim corpus
        corpusn = matutils.Sparse2Corpus(scipy.sparse.csr_matrix(data_dtmn.transpose()))

        # Create the vocabulary dictionary
        id2wordn = dict((v, k) for k, v in cvn.vocabulary_.items())

        return [corpusn, id2wordn]


    def regular_model(self, corpus, id2word):
        # Now that we have the corpus (term-document matrix) and id2word (dictionary of location: term),
        # we need to specify two other parameters as well - the number of topics and the number of passes
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=2, passes=10)
        self.write_model_to_file(lda, "LDA_2_topics")

        # LDA for num_topics = 3
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=3, passes=10)
        self.write_model_to_file(lda, "LDA_3_topics")

        # LDA for num_topics = 4
        lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=4, passes=10)
        self.write_model_to_file(lda, "LDA_4_topics")


    def nounsonly(self, corpusn, id2wordn):
        # Let's start with 2 topics
        ldan = models.LdaModel(corpus=corpusn, num_topics=2, id2word=id2wordn, passes=10)
        self.write_model_to_file(ldan, "LDA_2_topics_nouns")

        # Let's try topics = 3
        ldan = models.LdaModel(corpus=corpusn, num_topics=3, id2word=id2wordn, passes=10)
        self.write_model_to_file(ldan, "LDA_3_topics_nouns")

        # Let's try 4 topics
        ldan = models.LdaModel(corpus=corpusn, num_topics=4, id2word=id2wordn, passes=10)
        self.write_model_to_file(ldan, "LDA_4_topics_nouns")


    def nouns_and_adj(self, corpusna, id2wordna):
        # Let's start with 2 topics
        ldana = models.LdaModel(corpus=corpusna, num_topics=2, id2word=id2wordna, passes=10)
        self.write_model_to_file(ldana, "LDA_2_topics_nouns_and_adj_pas_10")

        # Let's try 3 topics
        ldana = models.LdaModel(corpus=corpusna, num_topics=3, id2word=id2wordna, passes=10)
        self.write_model_to_file(ldana, "LDA_3_topics_nouns_and_adj_pas_10")

        # Let's try 4 topics
        ldana = models.LdaModel(corpus=corpusna, num_topics=4, id2word=id2wordna, passes=10)
        self.write_model_to_file(ldana, "LDA_4_topics_nouns_and_adj_pas_10")

        # Our final LDA model (for now)
        ldana = models.LdaModel(corpus=corpusna, num_topics=4, id2word=id2wordna, passes=80)
        self.write_model_to_file(ldana, "LDA_4_topics_nouns_and_adj_pas_80")

        return ldana

    def list_topic_per_article(self, ldana, corpusna, data_dtmna):
        # Let's take a look at which topics each transcript contains
        corpus_transformed = ldana[corpusna]
        list_with_all_topics = []
        for topics in corpus_transformed:
            list_of_topics = []
            for topic in topics:
                list_of_topics.append(topic[0])
            list_with_all_topics.append(list_of_topics)

        topics_per_article = list(zip(list_with_all_topics, data_dtmna.index))

        f = open("topics_per_article", "w")
        for topics in topics_per_article:
            f.write(str(topics))
            f.write("\n")
        f.close()


    def nouns_adj(self, text):
        # Let's create a function to pull out nouns from a string of text
        '''Given a string of text, tokenize the text and pull out only the nouns and adjectives.'''
        is_noun_adj = lambda pos: pos[:2] == 'NN' or pos[:2] == 'JJ'
        tokenized = word_tokenize(text)
        nouns_adj = [word for (word, pos) in pos_tag(tokenized) if is_noun_adj(pos)]
        return ' '.join(nouns_adj)


    def nouns(self, text):
        '''Given a string of text, tokenize the text and pull out only the nouns.'''
        is_noun = lambda pos: pos[:2] == 'NN'
        tokenized = word_tokenize(text)
        all_nouns = [word for (word, pos) in pos_tag(tokenized) if is_noun(pos)]
        return ' '.join(all_nouns)


    def print_arguments(self):
        print("Arguments:")

        print("")


if __name__ == '__main__':
    m = main()
    m.start()










