#!/usr/bin/env python
import pandas as pd
import argparse
import feedparser


# Metadata
__program__ = "week1"
__author__ = "Britt Vink"
__maintainer__ = "Britt Vink"
__email__ = "b.vink@st.hanze.nl"
__version__ = 1.0
__description__ = "{} is a program developed and maintained by {}. " .format(__program__,
                                        __author__,)

class main():
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()
        self.input_file = getattr(arguments, 'input')


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
                            type=str,
                            required=True,
                            help="The path to the input file.")

        return parser.parse_args()

    def start(self):
        # Print arguments
        self.print_arguments()

        # Make a list with urls from inputfile

        list = []
        with open(self.input_file) as f:
            lines = f.readlines()
            for line in lines:
                list.append(line.strip())

        posts = []
        for url in list:
            NewsFeed = feedparser.parse(url)

            # Get information from all posts in url
            for i in range(len(NewsFeed.entries)):
                entry = NewsFeed.entries[i]

                # Get ID
                split_url = entry.id.split("/")
                last = split_url[-1]
                id = last.split('.')

                # Add post to list "posts"
                posts.append((entry.title, entry.link, entry.summary, entry.published, id[0]))

        # Add posts to dataframe
        df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])
        df.to_csv('out.txt', index=False)

    def print_arguments(self):
        print("Arguments:")
        print("  > Inputfile : {}".format(self.input_file))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()