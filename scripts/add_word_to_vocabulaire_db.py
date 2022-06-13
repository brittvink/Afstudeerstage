"""
File:         Database.py
Created:      2022/03/08
Last Changed: 2022/03/11
Author:       B.Vink

This pythonscript is used to read a text file and put the data in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""

from getpass import getpass
from mysql.connector import connect, Error
import uuid
import numpy as np
import argparse
import os
import pandas as pd
from getpass import getpass


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
    """ This pythonclass is used to read a text file and put the data in a MySQL Database"""
    def __init__(self):
        # Get the command line arguments.
        arguments = self.create_argument_parser()
        self.input = getattr(arguments, 'input')
        self.user = getattr(arguments, 'user')
        self.password = getattr(arguments, 'password')


    @staticmethod
    def create_argument_parser():
        """
                Creates a argument parser
                :return:  ArgumentParser with input, user and password
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
                            type=str,
                            required=True,
                            help="Path to input file")

        parser.add_argument("-u",
                            "--user",
                            type=str,
                            required=True,
                            help="database user name")

        parser.add_argument("-p",
                            "--password",
                            type=str,
                            required=True,
                            help="database password")

        return parser.parse_args()


    def start(self):
        """
                Return nothing.

                :param self.input: String (document name)
                :param self.name: String (database name)
                :param self.password: String (database password)

                The input file is readed. If the parent - child combination is not in the db yet, it will be added.
                """
        self.print_arguments()

        df = pd.read_csv(self.input, header=None)

        # Delete row if no child is given in the file
        dfNew = df.dropna(subset=[1])

        # Make connection with db
        cnx = self.make_db_connection()

        # For each row, put values in db
        for index, row in dfNew.iterrows():
            self.add_word_to_db(row[0], row[1], cnx)

        cnx.close()


    def make_db_connection(self):
        """
        Returns nothing

        Connection with database is made
        """
        try:
            connection = connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database="KCBBE2",
            )
            return connection
        except Error as e:
            print(e)


    def add_word_to_db(self, parent, child, cnx):
        """
        Add parent and child to database table: "Vocabuliar"

        :param parent: string
        :param child: string
        :return: nothing
        """

        cursor = cnx.cursor()

        # Query to create table if this one doesn't exists yet
        create_information_table_query = """
                    CREATE TABLE IF NOT EXISTS database_Vocabulair(
                    id VARCHAR(100),
                    key_id VARCHAR (100),
                    word VARCHAR(100),
                    PRIMARY KEY (id))
        """

        # Execute query to create table
        cursor.execute(create_information_table_query)
        cnx.commit()

        # Put values in table
        sql = "INSERT INTO database_Vocabulair (id, key_id, word) VALUES ('" + str(uuid.uuid1().int) + "', '" + parent + "', '" + child + "')"
        cursor.execute(sql)
        cnx.commit()

        cursor.close()


    def print_arguments(self):
        """
        Arguments are printed in the terminal

        :return: nothing
        """

        print("Arguments:")
        print("  > File : {}".format(self.input))
        print("  > Username: {}".format(self.user))
        print("  > Password: {}".format(self.password))


if __name__ == '__main__':
    m = main()
    m.start()