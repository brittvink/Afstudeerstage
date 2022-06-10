#!/usr/bin/env python
# import pandas for data wrangling
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from gensim.models import KeyedVectors
import os
import argparse


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
        self.df1 = getattr(arguments, 'dataframe1')
        self.df2 = getattr(arguments, 'dataframe2')


        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'difference_between_df', str(self.df1.split("/")[-1] + "_vs_" + self.df2.split("/")[-1]))
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

        parser.add_argument("-df1",
                            "--dataframe1",
                            required=True,
                            type=str,
                            help="The path to the input directory.")

        parser.add_argument("-df2",
                            "--dataframe2",
                            required=True,
                            type=str,
                            help="The path to the input directory.")



        return parser.parse_args()

    def start(self):
        # df_tokens = pd.read_pickle("processing/df_article_distance_tokenized_data.pkl")
        # df_keys = pd.read_pickle("processing/df_article_distance_keywords.pkl")

        df_tokens = pd.read_pickle(self.df1)
        df_keys = pd.read_pickle(self.df2)

        print(df_tokens)
        print(df_keys)

        df_difference = df_tokens.subtract(df_keys)
        print(df_difference)

        df_difference = df_difference.pow(2)
        df_difference['total'] = df_difference.sum(axis=1)
        print(df_difference)

        plt.hist(df_difference.total.tolist(), bins=30, color="orange")

        plt.xlabel('Difference')
        plt.title("Histogram of difference between similarity data and keywordset")
        plt.ylabel("Number Of Articles")
        plt.savefig(os.path.join(self.outdir, "difference_between.png"))


if __name__ == '__main__':
    m = main()
    m.start()

