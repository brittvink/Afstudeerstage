#!/usr/bin/env python

"""
File:         zoeken.py
Created:      2022/02/17
Last Changed: 2022/02/22
Author:       B.Vink

This pythonscript is used to read a database table and find all results that match input filters

The filters are given with the input argument (-s).
The database is readed and results are printed in terminal
"""

# Third party inputs
import argparse
from getpass import getpass
from mysql.connector import connect, Error

# Metadata
__program__ = "search in database"
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

        # Try to connect with database
        try:
            with connect(
                    host="localhost",
                    user=input("Enter username: "),
                    password=getpass("Enter password: "),
                    database="KCBBE",
            ) as connection:
                # print connection
                print(connection)

                cursor = connection.cursor()

                # Search for every searched word
                for word in self.search_string:
                    # Execute search query
                    cursor.execute("SELECT title FROM information where title LIKE '%" + word + "%' OR summary LIKE '%" + word + "%'")

                    # Fetch all results
                    result = cursor.fetchall()

                    # Loop through the results and print them
                    for row in result:
                        print(row)
                        print("\n")

        except Error as e:
            # Show error if connection could not be made
            print(e)

    def print_arguments(self):
        print("Arguments:")
        print("  > Search string : {}".format(self.search_string))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()