#!/usr/bin/env python

"""
File:         Database.py
Created:      2022/03/08
Last Changed: 2022/03/11
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
__program__ = "fill filters"
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


                # Find the vocalulaire of the input word and make a list of the result
                sql = "select word from database_Vocabulair where key_id ='" + self.input_word +  "'"
                cursor.execute(sql)
                vocabulair_list = [item[-1] for item in cursor.fetchall()]
                vocabulair_list.append(self.input_word)


                # Try to find articles that match
                # And make a list of the results
                list_with_articles = []
                for word in vocabulair_list:
                    sql = "select * from database_Information where title like '%" \
                          + word +\
                          "%' or title like '%" \
                          + word.capitalize() +\
                          "%'or summary like '%" \
                          + word + \
                          "%'or summary like '%" \
                        + word.capitalize() + "%'"
                    cursor.execute(sql)
                    list_of_articles = [item[-1] for item in cursor.fetchall()]
                    list_with_articles.append(list_of_articles)

                # Make one list of list of lists
                list_with_articles = [item for sublist in list_with_articles for item in sublist]
                ## Delete duplicates from the list
                list_with_articles = list(set(list_with_articles))

                # Add articles to database
                for article in list_with_articles:
                    id = uuid.uuid1()
                    id_num = id.int
                    sql = 'INSERT INTO KCBBE2.database_Search (id, search_id, article_id) VALUE("' + str(id_num) + '", "' + self.input_word + '", "' + article + '")'
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
        print("  > Inputfile : {}".format(self.input_word))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()