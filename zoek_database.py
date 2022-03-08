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
import argparse
from getpass import getpass
from mysql.connector import connect, Error
import uuid

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
        self.input_word = getattr(arguments, 'input')


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
        # Try to make a connection with the database
        try:
            with connect(
                    host="localhost",
                    user="root",
                    password="HoiAap12",
                    database="KCBBE2",
            ) as connection:

                # Query to create table if this one doesn't exists yet
                create_information_table_query = """
                    CREATE TABLE IF NOT EXISTS database_Search(
                    id VARCHAR(500),
                    search_id VARCHAR (100),
                    article_id VARCHAR(100),
                    PRIMARY KEY (id)
                    )
                """

                # Execute query to create table
                with connection.cursor() as cursor:
                    cursor.execute(create_information_table_query)
                    connection.commit()

                # get cursor object
                cursor = connection.cursor()

                id_voor_db = uuid.uuid1()
                print(str(id_voor_db.int))

                sql = "select * from database_Information where title like '%" + self.input_word + "%' or summary like '%" + self.input_word + "%'"
                cursor.execute(sql)
                row = [item[-1] for item in cursor.fetchall()]

                for article in row:
                    print(type(article))
                    id = uuid.uuid1()
                    id_num = id.int
                    sql = 'INSERT INTO KCBBE2.database_Search (id, search_id, article_id) VALUE ("' + str(id_num) + '", "' + self.input_word + '", "' + article + '")'
                    print(sql)
                    cursor.execute(sql)
                    connection.commit()


                # Close connection
                cursor.close()
                connection.close()

        # Throw error if trying to connect fails
        except Error as e:
            print(e)


    def print_arguments(self):
        print("Arguments:")
        # print("  > Inputfile : {}".format(self.input_file))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()