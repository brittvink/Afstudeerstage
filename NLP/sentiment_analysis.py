#!/usr/bin/env python
import numpy as np
import pandas as pd
import argparse
from textblob import TextBlob
import matplotlib.pyplot as plt
import math


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
        data = pd.read_pickle("df.pkl")
        self.create_polarity_plot(data)
        self.create_plot_polarty_verloop(data)


    def create_polarity_plot(self, data):
        # Create quick lambda functions to find the polarity and subjectivity of each routine
        pol = lambda x: TextBlob(x).sentiment.polarity
        sub = lambda x: TextBlob(x).sentiment.subjectivity

        data['polarity'] = data['text'].apply(pol)
        data['subjectivity'] = data['text'].apply(sub)

        plt.rcParams['figure.figsize'] = [10, 8]

        for index, article in enumerate(data.index):
            x = data.polarity.loc[article]
            y = data.subjectivity.loc[article]
            plt.scatter(x, y, color='blue')
            plt.text(x + .001, y + .001, data.index[index], fontsize=1)
            plt.xlim(-.01, .12)

        plt.title('Sentiment Analysis', fontsize=20)
        plt.xlabel('<-- Negative -------- Positive -->', fontsize=15)
        plt.ylabel('<-- Facts -------- Opinions -->', fontsize=15)

        plt.savefig('words_said_plot.png')


    def create_plot_polarty_verloop(self, data):
        # Let's create a list to hold all of the pieces of text
        list_pieces = []
        for t in data.text:
            split = self.split_text(t)
            list_pieces.append(split)

        # Calculate the polarity for each piece of text
        polarity_transcript = []
        for lp in list_pieces:
            polarity_piece = []
            for p in lp:
                polarity_piece.append(TextBlob(p).sentiment.polarity)
            polarity_transcript.append(polarity_piece)

        print(polarity_transcript)

        # Show the plot for all comedians
        for index, article in enumerate(data.index):
            plt.rcParams['figure.figsize'] = [16, 12]
            plt.plot(polarity_transcript[index])
            plt.title(data.index[index])
            plt.ylim(ymin=-.2, ymax=.3)
            name = "polarity/" + article + ".png"
            plt.savefig(name)
            plt.close()

        print("polarity plots made")


    def split_text(self, text, n=10):
        '''Takes in a string of text and splits into n equal parts, with a default of 10 equal parts.'''

        # Calculate length of text, the size of each chunk of text and the starting points of each chunk of text
        length = len(text)
        size = math.floor(length / n)
        start = np.arange(0, length, size)

        # Pull out equally sized pieces of text and put it into a list
        split_list = []
        for piece in range(n):
            split_list.append(text[start[piece]:start[piece] + size])
        return split_list

    def print_arguments(self):
        print("Arguments:")

        print("")


if __name__ == '__main__':
    m = main()
    m.start()



