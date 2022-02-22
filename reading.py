#!/usr/bin/env python

"""
File:         reading.py
Created:      2022/02/17
Last Changed: 2022/02/22
Author:       B.Vink

This pythonscript is used to fetch RSS data and write the data to a text file

The RSS links can be given as a input argument (-i). It is suppose to be a textfile with on each line the link of an RSS feed.
The data is readed and put in a dataframe
The dataframe is written to a textfile (name of file given with argument output (-o))
"""

# Third party imports.
import pandas as pd
import argparse
import feedparser

# Metadata
__program__ = "read RSS feeds"
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
        self.output_file = getattr(arguments, 'output')

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

        parser.add_argument("-o",
                            "--output",
                            type=str,
                            required=True,
                            help="the name of the output file")

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

        # Parse data from urls in list
        posts = []
        for url in list:
            NewsFeed = feedparser.parse(url)

            # Get information from all posts in url
            for i in range(len(NewsFeed.entries)):
                entry = NewsFeed.entries[i]
                id = self.create_id(entry)

                # Add post to list "posts"
                posts.append((entry.title, entry.link, entry.summary, entry.published, id))

        # Add posts to dataframe
        df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])

        # Write dataframe to outputfile
        df.to_csv(self.output_file, index=False)

    def create_id(self, entry):
        # Get ID
        id = entry.id + entry.title[:30]
        id = id.split("www.")[1]

        # Remove spaces, points and slaches
        remove_characters = [".", " ", "/"]
        for character in remove_characters:
            id = id.replace(character, "_")

        # Make sure all ID's have the same length
        if (len(id)) < 80:
            difference = 80 - len(id)
            string_to_add = ""
            for x in range(difference):
                string_to_add += "_"
            id += string_to_add

        # Return ID
        return id

    def print_arguments(self):
        print("Arguments:")
        print("  > Inputfile : {}".format(self.input_file))
        print("  > Outputfile : {}".format(self.output_file))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()