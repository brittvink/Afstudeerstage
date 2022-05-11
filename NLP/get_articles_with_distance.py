#!/usr/bin/env python

import pandas as pd
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
        self.minsim = getattr(arguments, 'min_sim')
        self.max_art = getattr(arguments, 'max_art')
        self.article = getattr(arguments, 'article')

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
        self.print_arguments()

        df = pd.read_pickle("df3.pkl")
        dictionary_distance = df.set_index(df.index).T.to_dict()

        # Get 3 most related of input
        # value = "sciencedaily_com_releases_2022_02_220215113437_htmClimate_change_and_extreme_wea"
        print(self.article)
        top_most_similar = self.find_similair([(self.article, 0)], dictionary_distance)
        top_most_similar = list(top_most_similar.values())
        top_most_similar =  [item for sublist in top_most_similar for item in sublist]

        # exit()
        # distance_article = dictionary_distance.get(self.article)
        # distance_article = dict(sorted(distance_article.items(), key=lambda item: item[1]))
        # top_most_similar = list(distance_article.items())[1:self.max_art + 1]

        newdict = self.find_similair(top_most_similar, dictionary_distance)


    def find_similair(self, top_most_similar, dictionary_distance):
        return_list = {}
        for article, similarity in top_most_similar:
            return_list[article] = []
            print("\t" + article + " - " + str(similarity))
            new_dict = dictionary_distance.get(article)
            new_dict = dict(sorted(new_dict.items(), key=lambda item: item[1]))
            for article_child, similarity_child in list(new_dict.items())[1: self.max_art + 1]:
                if similarity_child < self.minsim:
                    print("\t\t" + article_child + " - " + str(similarity_child))
                    return_list[article].append((article_child, similarity_child))
        return return_list


    def print_arguments(self):
        print("Arguments:")
        print("  > Input article : {}".format(self.article))

        print("  > Minimale similarity : {}".format(self.minsim))
        print("  > Maximal number of articles : {}".format(self.max_art))



if __name__ == '__main__':
    m = main()
    m.start()




