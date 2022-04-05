#!/usr/bin/env python
import pandas as pd
import argparse
import os
import glob



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
        self.input = getattr(arguments, 'input')

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
        parser.add_argument("-i",
                            "--input",
                            default="/Users/brittvink/Desktop/KCBBE/website/media/articles",
                            type=str,
                            help="The path to the input directory.")

        return parser.parse_args()

    def start(self):
        self.print_arguments()
        articledict = self.readfiles()
        self.make_df(articledict)

    def readfiles(self):
        os.chdir(self.input)

        list_of_articles = []
        for file in glob.glob("*.txt"):
            list_of_articles.append(file)

        article_dictionary = {}
        for file in list_of_articles:
            with open(file) as f:
                lines = f.readlines()
                if len(lines) != 1:
                    print(file)
                    print(len(lines))
                article_dictionary[file] = lines

        os.chdir("/Users/brittvink/Desktop/NLT")

        return article_dictionary

    def make_df(self, article_dictionary):
        df = pd.DataFrame.from_dict(article_dictionary).transpose()
        df.columns = ["text"]
        df.to_pickle("df.pkl")
        return df


    def print_arguments(self):
        print("Arguments:")
        print("  > Input : {}".format(self.input))

        print("")

if __name__ == '__main__':
    m = main()
    m.start()




