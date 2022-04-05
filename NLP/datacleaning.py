#!/usr/bin/env python
import pandas as pd
import argparse
import re
import string


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
        self.cleaning()


    def cleaning(self):
        df = pd.read_pickle("df.pkl")

        round1 = lambda x: self.clean_text_round1(x)
        data_clean = pd.DataFrame(df.text.apply(round1))

        round2 = lambda x: self.clean_text_round2(x)
        data_clean = pd.DataFrame(data_clean.text.apply(round2))

        data_clean.to_pickle("data_clean.pkl")


    # Apply a first round of text cleaning techniques
    def clean_text_round1(self, text):
        '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text


    def clean_text_round2(self, text):
        '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
        text = re.sub('[‘’“”…]', '', text)
        text = re.sub('\n', '', text)
        return text


    def print_arguments(self):
        print("Arguments:")
        print("")

if __name__ == '__main__':
    m = main()
    m.start()




