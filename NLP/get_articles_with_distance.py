#!/usr/bin/env python

import pandas as pd
import argparse
import numpy as np

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

        # df = pd.read_pickle("processing/df_article_distance_tokenized_data.pkl")
        df = pd.read_pickle("TF-IDF/tf-idf_cleaned_text.pkl")
        # #
        df.replace(0, np.nan, inplace=True)
        #
        df.replace(0.05942325270774634, np.nan, inplace=True)
        var1 = df.min(numeric_only=True).min()
        print(var1)
        df_min = df[df == var1].dropna(how='all')
        print(df_min.index)
        #
        # var1 = df.max(numeric_only=True).max()
        # print(var1)
        # df_max = df[df == var1].dropna(how='all')
        # print(df_max)
        # #
        # df_max = df_max.dropna(axis=1, how='all')
        # # df_max = df_max.drop(columns=["sciencedaily_com_releases_2010_01_100129092633_htmFatality_Rates_Among_Young_Dru",
        # #                               "sciencedaily_com_releases_2015_07_150716112252_htmDespite_new_information,_Pluto",
        # #                               "sciencedaily_com_releases_2010_05_100507101840_htmTreatment_of_Helicobacter_pylo",
        # #                               "sciencedaily_com_releases_2016_06_160609093513_htmResearchers_map_mosquitoes_tha",
        # #                               "sciencedaily_com_releases_2009_05_090529112056_htmKnock-Out_Drugs:_Narrow_Window",
        # #                               "sciencedaily_com_releases_2021_10_211018100043_htmRunning_shoe_material_inspired",
        # #                               "sciencedaily_com_releases_2020_10_201022144549_htmHow_genetic_variation_gives_ri"])
        # df_max.columns = [''] * len(df_max.columns)
        #
        # print(df_max)
        # print(df_max.index)



        # df = pd.read_pickle("processing/df_article_distance_tokenized_data.pkl")
        # df = pd.read_pickle("TF-IDF/tf-idf_cleaned_text.pkl")
        # print(df)
        # dictionary_distance = df.set_index(df.index).T.to_dict()
        # print(dictionary_distance)
        # exit()
        #
        # # Get 3 most related of input
        # # value = "sciencedaily_com_releases_2022_02_220215113437_htmClimate_change_and_extreme_wea"
        # print(self.article)
        # top_most_similar = self.find_similair([(self.article, 0)], dictionary_distance)
        # print(top_most_similar)
        # top_most_similar = list(top_most_similar.values())
        # top_most_similar =  [item for sublist in top_most_similar for item in sublist]
        #
        # # exit()
        # # distance_article = dictionary_distance.get(self.article)
        # # distance_article = dict(sorted(distance_article.items(), key=lambda item: item[1]))
        # # top_most_similar = list(distance_article.items())[1:self.max_art + 1]
        #
        # newdict = self.find_similair(top_most_similar, dictionary_distance)
        # print(newdict)


    def find_similair(self, top_most_similar, dictionary_distance):
        return_list = {}
        for article, similarity in top_most_similar:
            return_list[article] = []
            print("\t" + article + " - " + str(similarity))
            new_dict1 = dictionary_distance.get(article)
            new_dict = dict(sorted(new_dict1.items(), key=lambda item: item[1]))
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
        print("\n")
        print("\n")



if __name__ == '__main__':
    m = main()
    m.start()




