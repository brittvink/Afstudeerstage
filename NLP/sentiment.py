#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from textblob import TextBlob
import matplotlib.pyplot as plt
import math
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
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

        self.prefix = getattr(arguments, 'prefix')
        self.df = getattr(arguments, 'dataframe')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'sentiment/senetiment_plots', self.df)
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

        parser.add_argument("-df",
                            "--dataframe",
                            type=str,
                            required=True,
                            help="dataframe")


        return parser.parse_args()


    def start(self):
        self.print_arguments()

        logging.basicConfig(filename=os.path.join(self.outdir, "sentiment.log"),
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)


        data = pd.read_pickle(self.df)


        logging.info(data.shape)

        listyear = []
        publishedlist = data['published'].tolist()
        for published in publishedlist:
            published = published.split(" ")
            listyear.append(published[3])

        data['year'] = listyear
        data["year"] = data["year"].astype("int")


        listyear = []
        publishedlist = data['published'].tolist()
        for published in publishedlist:
            stringe = ""
            published = published.split(" ")
            print(published)
            stringe += published[3]
            if published[2] == 'Jan':
                stringe += "-01-"
            if published[2] == 'Feb':
                stringe += "-02-"
            if published[2] == 'Mar':
                stringe += "-03-"
            if published[2] == 'Apr':
                stringe += "-04-"
            if published[2] == 'May':
                stringe += "-05-"
            if published[2] == 'Jun':
                stringe += "-06-"
            if published[2] == 'Jul':
                stringe += "-07-"
            if published[2] == 'Aug':
                stringe += "-08-"
            if published[2] == 'Sep':
                stringe += "-09-"
            if published[2] == 'Oct':
                stringe += "-10-"
            if published[2] == 'Nov':
                stringe += "-11-"
            if published[2] == 'Dec':
                stringe += "-12-"
            stringe += published[1]
            listyear.append(stringe)


        data['date'] = listyear
        data["date"] = data["date"].astype("datetime64")

        pol = lambda x: TextBlob(x).sentiment.polarity
        sub = lambda x: TextBlob(x).sentiment.subjectivity

        data['polarity'] = data['text'].apply(pol)
        data['subjectivity'] = data['text'].apply(sub)

        self.plot(data, "subjectivity")
        self.plot(data, "polarity")

        df_2022 = data.loc[data['year'] > 2021]
        print(df_2022)
        self.plot(df_2022, "subjectivity", True)
        self.plot(df_2022, "polarity", True)


    def plot(self, data, kind, ingezoomd=False):
        fig, ax = plt.subplots(figsize=(15, 4))

        plt.plot(data['date'].sort_index(), data[kind])
        plt.legend()
        ax.set_ylabel(kind)

        # Get second axis
        ax2 = ax.twinx()
        plt.plot(data['date'].value_counts().sort_index(), color="orange")
        plt.legend()
        ax2.set_ylabel("Number of articles")

        plt.xlabel("Date")
        if ingezoomd is True:
            plt.title("lineplot of {} in articles published in 2022".format(kind))
        else:
            plt.title("lineplot of {} in articles".format(kind))

        outpath = os.path.join(self.outdir,
                               "{}_lineplot_{}_alleen2022_{}.png".format(self.prefix, kind, ingezoomd))
        plt.savefig(outpath)
        plt.close()


    def print_arguments(self):
        print("Arguments:")

        print("")

if __name__ == '__main__':
    m = main()
    m.start()