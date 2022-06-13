#!/usr/bin/env python

"""
File:         get_data.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is used to get data from the Database

The path to the full text of all articles is given with the input argument (-i).
The data is fetched, readed and put in the dataframe
"""


import pandas as pd
import argparse
import os
import glob
from mysql.connector import connect, Error

# Metadata
__program__ = "Get data"
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
    """ Iets leuks"""
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()
        self.input = getattr(arguments, 'input')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'data')
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    @staticmethod
    def create_argument_parser():
        """
        Creates a argument parser
        :return:  ArgumentParser with input
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

        parser.add_argument("-i",
                            "--input",
                            default="/Users/brittvink/Desktop/KCBBE/website/media/articles",
                            type=str,
                            help="The path to the input directory.")

        return parser.parse_args()


    def start(self):
        """
        All text files are saved in a dictionary.
        Than all data from the database is fetched and put in a dataframe
        The dictionary is also added to the dataframe. The whole dataframe is saved.

                :return: nothing

        """

        self.print_arguments()

        articledict = self.readfiles()

        df = self.make_df(articledict)

        # Try to connect with database
        cnx = self.make_db_connection()
        cursor = cnx.cursor()

        cursor.execute("SELECT * FROM database_Articles")

        # Fetch all results
        df1 = pd.DataFrame(cursor.fetchall(), columns=['title', 'link', 'summary', 'published', 'id', 'rss'])
        cursor.close()
        cnx.close()

        lisje = []
        for i in df.index.tolist():
            i = i.split(".")
            lisje.append(i[0])

        df['index_goed'] = lisje
        df2 = df.set_index('index_goed').join(df1.set_index('id'))

        df2.to_pickle(os.path.join(self.outdir,"Information_joined.pkl"))


    def make_db_connection(self):
        """
        Connection with database is made
                :return: nothing

        """

        try:
            connection = connect(
                host="localhost",
                user="root",
                password="HoiAap12",
                database="KCBBE2",
            )
            return connection
        except Error as e:
            print(e)


    def readfiles(self):
        """
        Read files and put them in a Dictionary, that is returned
                :return: dictionary

        """

        os.chdir(self.input)

        list_of_articles = []
        for file in glob.glob("*.txt"):
            list_of_articles.append(file)

        article_dictionary = {}
        for file in list_of_articles:
            with open(file) as f:
                lines = f.readlines()
                article_dictionary[file] = lines

        os.chdir("/Users/brittvink/Desktop/Afstudeerstage/NLP")

        return article_dictionary


    def make_df(self, article_dictionary):
        """
        Make df of a dictionary, save it and return the dataframe
                :return: dataframe

        """

        df = pd.DataFrame.from_dict(article_dictionary).transpose()
        df.columns = ["text"]
        df.to_pickle(os.path.join(self.outdir,"Information.pkl"))
        return df


    def print_arguments(self):
        """
        Arguments are printed in the terminal
                :return: nothing

        """
        print("Arguments:")
        print("  > Input : {}".format(self.input))
        print("")


if __name__ == '__main__':
    m = main()
    m.start()




