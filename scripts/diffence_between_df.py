#!/usr/bin/env python

"""
File:         difference_between_df.py
Created:      n.v.t
Last Changed: 2022/06/10
Author:       B.Vink

This pythonscript is calculate the differences between two dataframes and plot these differences

The data is given with the df1 and df2 arguments (-df1 and -df2).
"""


import pandas as pd
import matplotlib.pyplot as plt
import os
import argparse


# Metadata
__program__ = "Calculate difference between dataframes"
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
        self.df1 = getattr(arguments, 'dataframe1')
        self.df2 = getattr(arguments, 'dataframe2')

        # Set variables.
        self.outdir = os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'difference_between_df', str(self.df1.split("/")[-1] + "_vs_" + self.df2.split("/")[-1]))
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)


    @staticmethod
    def create_argument_parser():
        """
        Creates a argument parser
        :return:  ArgumentParser with df1 and df2
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
        """
        The difference between two dataframes is calculated.
        The difference is than be powered by two, so all values are positive.
        A histrogram is made showing the difference between the dataframes
        :return: nothing
        """

        df_tokens = pd.read_pickle(self.df1)
        df_keys = pd.read_pickle(self.df2)

        df_difference = df_tokens.subtract(df_keys)

        df_difference = df_difference.pow(2)
        df_difference['total'] = df_difference.sum(axis=1)

        plt.hist(df_difference.total.tolist(), bins=30, color="orange")

        plt.xlabel('Difference')
        plt.title("Histogram of difference between similarity data and keywordset")
        plt.ylabel("Number Of Articles")
        plt.savefig(os.path.join(self.outdir, "difference_between.png"))


if __name__ == '__main__':
    m = main()
    m.start()