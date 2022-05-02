#!/usr/bin/env python

import argparse
from mysql.connector import connect, Error
import uuid
import re

"""
File:         Database.py
Created:      2022/03/14
Last Changed: 2022/04/28
Author:       B.Vink

This pythonscript is used to read a text file with filter words.
All articles that match the filter will be put in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""

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
        self.input_file = getattr(arguments, 'input_file')
        self.user = getattr(arguments, 'user')
        self.password = getattr(arguments, 'password')


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
                            "--input_file",
                            type=str,
                            required=True,
                            help="The path to the input file.")

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

        :param self.input_word: String
        :param self.name: String (database name)
        :param self.password: String (database password)

        A vocabulaire of the inputword is searched.
        If no vocabulaire found the inputword is the whole vocabulair
        For all the words of the vocabulaire articles are found that have this word in the title or summary.
        Articles that are found using the inputword are put in the databasetable: "database_Search", using an ID, the inputword and the article ID
        """

        self.print_arguments()

        with open(self.input_file) as f:
            lines = f.readlines()

        cnx = self.make_db_connection()
        cursor = cnx.cursor()

        self.create_table(cnx, cursor)

        for word in lines:
            word = word.strip()
            print(word)
            self.filter(word, cnx, cursor)

        # Close connection
        cursor.close()
        cnx.close()


    def make_db_connection(self):
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


    def create_table(self, cnx, cursor):
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
        cursor.execute(create_information_table_query)
        cnx.commit()


    def find_vocabulaire(self, cursor, filter_word):
        sql = "select word from database_Vocabulair where key_id ='" + filter_word + "'"
        cursor.execute(sql)
        vocabulair_list = [item[-1] for item in cursor.fetchall()]

        if filter_word not in vocabulair_list:
            vocabulair_list.append(filter_word)

        return vocabulair_list


    def find_articles_with_filter(self, cursor, vocabulair_list):

        list_with_articles = []

        for word in vocabulair_list:
            # Make regex for every word in list
            if ' ' in word:
                word = word.split()
                my_regex = r"" + word[0] + "[ -]" + word[1] + r""
            else:
                my_regex = r"" + re.escape(word) + r""

            sql = "select * from database_Information where summary REGEXP '" + my_regex + "' or summary REGEXP'" + my_regex.capitalize() + "'"
            cursor.execute(sql)
            list_of_articles = [item[-1] for item in cursor.fetchall()]
            list_with_articles.append(list_of_articles)

        # Make one list of list of lists
        list_with_articles = [item for sublist in list_with_articles for item in sublist]
        # Delete duplicates from the list
        list_with_articles = list(set(list_with_articles))

        return list_with_articles


    def find_articles_to_add_to_db(self, cursor, list_with_articles, filter_word):
        sql = "select database_Information.id from database_Information INNER JOIN database_Search ON database_Information.id=database_Search.article_id where database_Search.search_id = '" + filter_word + "';"
        cursor.execute(sql)
        list_all_articles = [item[-1] for item in cursor.fetchall()]
        joined = list_with_articles + list_all_articles
        unique = [x for x in joined if joined.count(x) == 1]
        return unique


    def add_articles_to_db(self, cursor, cnx, unique, filter_word):
        for article in unique:
            id = uuid.uuid1().int
            sql = "INSERT INTO KCBBE2.database_Search (id, search_id, article_id) VALUE('" + str(
                    id) + "', '" + filter_word + "', '" + article + "')"
            try:
                cursor.execute(sql)
                cnx.commit()
            except Exception as e:
                print(e)
                sql = 'INSERT INTO KCBBE2.database_Search (id, search_id, article_id) VALUE("' + str(
                    id) + '", "' + filter_word + '", "' + article + '")'
                cursor.execute(sql)
                cnx.commit()


    def filter(self, filter_word, cnx , cursor):

        # Find the vocalulaire of the input word and make a list of the result
        vocabulair_list = self.find_vocabulaire(cursor, filter_word)

        # find articles that have match filter
        list_with_articles = self.find_articles_with_filter(cursor, vocabulair_list)

        # Find articles with this filter in de db, unique are the items that need to be added to the db
        unique = self.find_articles_to_add_to_db(cursor, list_with_articles, filter_word)

        # Add articles with filter to databasetable
        self.add_articles_to_db(cursor, cnx, unique, filter_word)





    def print_arguments(self):
        print("Arguments:")
        print("  > Inputfile : {}".format(self.input_file))
        print("")

if __name__ == '__main__':
    m = main()
    m.start()