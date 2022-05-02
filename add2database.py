#!/usr/bin/env python

import pandas as pd
import argparse
from mysql.connector import connect, Error
import feedparser
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path


"""
File:         Database.py
Created:      2022/02/17
Last Changed: 2022/02/22
Author:       B.Vink

This pythonscript is used to read a text file and put the data in a MySQL Database

The data is given with the input argument (-i).
The data is readed and put in the database
"""


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
                            "--input",
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

         :param self.input_file: String (txt file with RSS urls)
        :param self.name: String (database name)
        :param self.password: String (database password)

        For all the urls data is collected. The data is put in a dataframe and then added to the db, if it is not in there yet.
        """

        # Make a list with urls from inputfile
        urls = self.list_urls()

        # All data from the urls in a list
        posts = self.data_to_list(urls)

        # Add posts to dataframe
        df = pd.DataFrame(posts, columns=['title', 'link', 'summary', 'published', 'id'])

        # db connection
        cnx = self.make_db_connection()
        cursor = cnx.cursor()

        self.create_table(cnx, cursor)

        # creating column list for insertion
        cols = "`,`".join([str(i) for i in df.columns.tolist()])

        # Put data in table
        self.insert_data_in_table(df, cols, cursor, cnx)

        # Close connection
        cursor.close()
        cnx.close()


    def insert_data_in_table(self, df, cols, cursor, cnx):
        # Insert DataFrame records one by one if they are not in the database present yet.
        for i, row in df.iterrows():
            sql = "INSERT INTO `database_Information` (`" + cols + "`) VALUES (" + "%s," * (
                        len(row) - 1) + "%s) ON DUPLICATE KEY UPDATE id=id"
            cursor.execute(sql, tuple(row))

            # the connection is not autocommitted by default, so we must commit to save our changes
            cnx.commit()

            # Create text file with the article using the link
            self.create_text_file(row)


    def create_text_file(self, row):
        file = Path("KCBBE/website/media/articles/" + row[-1] + ".txt")
        if not file.is_file():
            result = self.main_webscraping(row[1])
            f = open(file, "w")
            f.write(result)
            f.close()


    def create_table(self, cnx, cursor):
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
        cursor.execute(create_information_table_query)
        cnx.commit()


    def main_webscraping(self, url):
        session = HTMLSession()
        getarticle_page = session.get(url)
        soup = BeautifulSoup(getarticle_page.content, 'html.parser')

        article = soup.find(id="text")
        text = article.find_all("p")

        string_met_info = ""
        for p in text:
            info = p.get_text()
            info = info.strip('"')
            info += " "
            string_met_info += info

        return string_met_info


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


    def list_urls(self):
        urls = []
        with open(self.input_file) as f:
            lines = f.readlines()
            for line in lines:
                urls.append(line.strip())
        return urls


    def data_to_list(self, urls):
        # Parse data from urls in list
        posts = []
        for url in urls:
            NewsFeed = feedparser.parse(url)

            # Get information from all posts in url
            for i in range(len(NewsFeed.entries)):
                entry = NewsFeed.entries[i]
                posts.append((entry.title, entry.link, entry.summary, entry.published, self.create_id(entry)))
        return posts


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
        print("")


if __name__ == '__main__':
    m = main()
    m.start()
