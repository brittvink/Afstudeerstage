#!/usr/bin/env python
import pandas as pd
import argparse
import pickle
from sklearn.feature_extraction.text import CountVectorizer

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
        self.dtm()

    def dtm(self):
        data_clean = pd.read_pickle("data_clean.pkl")

        # We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
        cv = CountVectorizer(stop_words='english')
        data_cv = cv.fit_transform(data_clean.text)
        data_dtm = pd.DataFrame(data_cv.toarray(),
                                columns=cv.get_feature_names())
        data_dtm.index = data_clean.index

        data_dtm.to_pickle("data_dtm.pkl")
        pickle.dump(cv, open("cv_dtm.pkl", "wb"))

        return [data_dtm, cv]


    def print_arguments(self):
            print("Arguments:")

            print("")

if __name__ == '__main__':
    m = main()
    m.start()






