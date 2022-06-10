#!/usr/bin/env python
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
        self.prefix = getattr(arguments, 'prefix')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'TF-IDF')
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

        parser.add_argument("-p",
                            "--prefix",
                            type=str,
                            required=True,
                            help="Prefix for the output file.")

        return parser.parse_args()


    def start(self):

        logging.basicConfig(filename=self.outdir + "/{}_logfile.log".format(self.prefix),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        logging.info("prefix: " + self.prefix)
        logging.info("outdir: " + self.outdir)


        documents = pd.read_pickle("pre_processing/df_preprocessed.pkl")
        documents["keywords_string"] = [' '.join(map(str, l)) for l in documents['keywords']]
        print(documents)

        # use tfidf by removing tokens that don't appear in at least 50 documents
        vect = TfidfVectorizer()

        # Fit and transform
        X = vect.fit_transform(documents.cleaned)

        df = pd.DataFrame(pairwise_distances(X))
        df.index = documents.index.tolist()
        df.columns = documents.index.tolist()
        df.to_pickle(os.path.join(self.outdir,"tf-idf_cleaned_text.pkl"))
        print(df)

        X = vect.fit_transform(documents.keywords_string)

        df = pd.DataFrame(pairwise_distances(X))
        df.index = documents.index.tolist()
        df.columns = documents.index.tolist()
        df.to_pickle(os.path.join(self.outdir, "tf-idf_keywords.pkl"))
        print(df)




if __name__ == '__main__':
    m = main()
    m.start()