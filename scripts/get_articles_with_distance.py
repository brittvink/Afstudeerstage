#!/usr/bin/env python

"""
File:         get_articles_with_distance.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to find the most similar aricles given a articleid

The article is given with the article argument (-a).
The minimal similarity is given with the min_sim argument.
The maximal number of articles shown is given with the max_art argument.
"""


import pandas as pd
import argparse
import numpy as np

# Metadata
__program__ = "Get articles with most similarity"
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
        self.minsim = getattr(arguments, 'min_sim')
        self.max_art = getattr(arguments, 'max_art')
        self.article = getattr(arguments, 'article')


    @staticmethod
    def create_argument_parser():
        """
        Creates a argument parser
        :return:  ArgumentParser with min_sim, max_art and article
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
        parser.add_argument("-ms",
                            "--min_sim",
                            type=int,
                            required=True,
                            help="minimal similaryt")

        parser.add_argument("-ma",
                            "--max_art",
                            type=int,
                            required=True,
                            help="maximal articles")

        parser.add_argument("-a",
                            "--article",
                            type=str,
                            required=True,
                            help="article")

        return parser.parse_args()


    def start(self):
        """
        This function makes a dictionary of the dataframe with all similarity scores.
        Than the dictionary get sorted so the article with the lowest score, so highest similariy, is saved.
        For all found similar articles this step is done once again.
        This minimal similarity has to given as well as the maximam number of articles the user wants to print
        The articles are printed as a tree

        :param article: String
        :param max_art: Interger
        :param min_sim: Interger
        :return: nothing
        """

        self.print_arguments()

        # df = pd.read_pickle("processing/df_article_distance_tokenized_data.pkl")
        df = pd.read_pickle("TF-IDF/tf-idf_cleaned_text.pkl")
        dictionary_distance = df.set_index(df.index).T.to_dict()

        # Get 3 most related of input
        top_most_similar = self.find_similair([(self.article, 0)], dictionary_distance)
        top_most_similar = list(top_most_similar.values())
        top_most_similar =  [item for sublist in top_most_similar for item in sublist]

        newdict = self.find_similair(top_most_similar, dictionary_distance)

        print(newdict)


    def find_similair(self, top_most_similar, dictionary_distance):
        """
        A list with the most similar articles for the items in the input list is returned.
        This list is made using the dictionary.

        :param top_most_similar: List
        :param dictionary_distance: Dictionary
        :return: List

        """
        return_list = {}

        for article, similarity in top_most_similar:
            return_list[article] = []
            new_dict1 = dictionary_distance.get(article)
            new_dict = dict(sorted(new_dict1.items(), key=lambda item: item[1]))
            for article_child, similarity_child in list(new_dict.items())[1: self.max_art + 1]:
                if similarity_child < self.minsim:
                    return_list[article].append((article_child, similarity_child))

        return return_list


    def print_arguments(self):
        """
                Arguments are printed in the terminal
                        :return: nothing

                """
        print("Arguments:")
        print("  > Input article : {}".format(self.article))
        print("  > Minimale similarity : {}".format(self.minsim))
        print("  > Maximal number of articles : {}".format(self.max_art))
        print("\n")


if __name__ == '__main__':
    m = main()
    m.start()




