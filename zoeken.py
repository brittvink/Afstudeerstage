#!/usr/bin/env python
import pandas as pd
import argparse
import feedparser
from getpass import getpass
from mysql.connector import connect, Error


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
        self.search_string = getattr(arguments, 'search')


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

        parser.add_argument("-s",
                            "--search",
                            type=str,
                            required=True,
                            default = [],
                            nargs='+',
                            help="The path to the input file.")

        return parser.parse_args()

    def start(self):
        # Print arguments
        self.print_arguments()

        try:
            with connect(
                    host="localhost",
                    user=input("Enter username: "),
                    password=getpass("Enter password: "),
                    database="KCBBE",
            ) as connection:
                print(connection)

                cursor = connection.cursor()

                print(self.search_string)
                for word in self.search_string:
                    print(word)
                    cursor.execute("SELECT title FROM information where title LIKE '%" + word + "%' OR summary LIKE '%" + word + "%'")
                    result = cursor.fetchall()
                    # Loop through the rows
                    for row in result:
                        print(row)
                        print("\n")

        except Error as e:
            print(e)

    def print_arguments(self):
        print("Arguments:")
        print("  > search string : {}".format(self.search_string))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()