
import yake
import argparse
import pandas as pd
from nltk import word_tokenize, pos_tag
import logging
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
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'pre_processing')
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

        df = pd.read_pickle("cleaned_data/df_cleaned.pkl")
        logging.info("dataframe shape" + str(df.shape))

        # Take keywords for each post and turn them into a textstring
        sentences = self.extract_keywords(df)
        logging.info("keywords token")

        # Get list keyword sets of all articles
        keyword_sets = [word_tokenize(i) for i in sentences]
        df["keywords"] = keyword_sets
        df.to_pickle(os.path.join(self.outdir,"df_pickle.pkl"))
        df = pd.read_pickle(os.path.join(self.outdir,"df_pickle.pkl"))
        print(df)


        data_tokenized = [word_tokenize(i) for i in df.cleaned.tolist()]
        df["tokenized"] = data_tokenized

        df.to_pickle(os.path.join(self.outdir,"df_preprocessed.pkl"))


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


    def print_arguments(self):
        print("Arguments:")


if __name__ == '__main__':
    m = main()
    m.start()