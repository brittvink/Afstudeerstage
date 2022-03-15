import argparse
from getpass import getpass
from mysql.connector import connect, Error
import uuid
import re

'''
14 maart
'''


def main_make_filter(input, all_articles):
    # Make connection with database
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
            sql = "select word from database_Vocabulair where key_id ='" + input + "'"
            cursor.execute(sql)
            vocabulair_list = [item[-1] for item in cursor.fetchall()]
            vocabulair_list.append(input)


            list_with_articles = []


            for word in vocabulair_list:
                # Make regex for every word in list
                if ' ' in word:
                    word = word.split()
                    my_regex = r"\b" + word[0] + "[ -]" + word[1] + r"\b"
                else:
                    my_regex = r"\b" + re.escape(word) + r"\b"

                for article in all_articles:
                    # Look per article if they match the regex
                    found = re.findall(my_regex, article.summary, re.IGNORECASE)
                    # If match, save
                    if found:
                        list_with_articles.append(article.id)

            # Remove duplicates
            list_with_articles = list(set(list_with_articles))

            # Only add items that are not for this filter in table yet
            from .models import Search
            all = Search.objects.filter(search_id=input)
            lijst = []
            for a in all:
                lijst.append(a.article_id)
            joined = list_with_articles + lijst
            unique = [x for x in joined if joined.count(x)==1]

            # Add articles with filter to databasetable
            for article in unique:
                id = uuid.uuid1().int
                sql = 'INSERT INTO KCBBE2.database_Search (id, search_id, article_id) VALUE("' + str(
                        id) + '", "' + input + '", "' + article + '")'
                cursor.execute(sql)
                connection.commit()

            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)
