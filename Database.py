#!/usr/bin/env python

"""
File:         Database.py
Created:      2022/02/17
Last Changed: 2022/02/22
Author:       B.Vink

This pythonscript is used to read a text file and put the data in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""

# Third party imports.
import pandas as pd
import argparse
from getpass import getpass
from mysql.connector import connect, Error

# Metadata
__program__ = "fill database"
__author__ = "Britt Vink"
__maintainer__ = "Britt Vink"
__email__ = "b.vink@st.hanze.nl"
__version__ = 1.0
__description__ = "{} is a program developed and maintained by {}. "\
                    .format(__program__, __author__)

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
        # Read input file
        df = pd.read_csv(self.input_file)

        # Try to make a connection with the database
        try:
            with connect(
                    host="localhost",
                    user=input("Enter username: "),
                    password=getpass("Enter password: "),
                    database="KCBBE2",
            ) as connection:
                # Print connection
                print(connection)

                # Query to create table if this one doesn't exists yet
                create_information_table_query = """
                    CREATE TABLE IF NOT EXISTS database_Information(
                    title VARCHAR(500),
                    link VARCHAR (100),
                    summary VARCHAR(1000),
                    published VARCHAR(100),
                    id VARCHAR (100),
                    PRIMARY KEY (id)
                    )
                """

                # Execute query to create table
                with connection.cursor() as cursor:
                    cursor.execute(create_information_table_query)
                    connection.commit()

                # get cursor object
                cursor = connection.cursor()

                # creating column list for insertion
                cols = "`,`".join([str(i) for i in df.columns.tolist()])

                # Insert DataFrame records one by one if they are not in the database present yet.
                for i, row in df.iterrows():
                    sql = "INSERT INTO `database_Information` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s) ON DUPLICATE KEY UPDATE id=id"
                    cursor.execute(sql, tuple(row))

                    # the connection is not autocommitted by default, so we must commit to save our changes
                    connection.commit()

                # Close connection
                cursor.close()
                connection.close()

        # Throw error if trying to connect fails
        except Error as e:
            print(e)


    def print_arguments(self):
        print("Arguments:")
        print("  > Inputfile : {}".format(self.input_file))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()