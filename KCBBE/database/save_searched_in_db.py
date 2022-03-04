from mysql.connector import connect, Error
from getpass import getpass
import uuid

"""
This function receives the topics and title keywords that were searced for,
even as the titles or articles that were found matching the search criteria.
This function adds the values to the database tables
"""


def main_search(searched_topic, searched_title, titles):
    #Try to make a connection with the database
    try:
        with connect(
                host="localhost",
                user="root",
                password="HoiAap12",
                database="KCBBE2",

        ) as connection:
            # get cursor object
            cursor = connection.cursor()

            # Query to create table if this one doesn't exists yet
            create_search_table_query = """
                CREATE TABLE IF NOT EXISTS database_search(
                id VARCHAR (100),
                key_id VARCHAR (100),
                article_id VARCHAR (100),
                PRIMARY KEY (id))
            """

            # Execute query to create table
            cursor.execute(create_search_table_query)
            connection.commit()

            # Query to create table if this one doesn't exists yet
            create_search_table_query = """
              CREATE TABLE IF NOT EXISTS database_search_info(
               id VARCHAR(100),
               searched_title VARCHAR (100),
               searched_topic VARCHAR (100),
                primary KEY (id))
            """

            # Execute query to create table
            cursor.execute(create_search_table_query)
            connection.commit()

            # Make a string of list with words
            string_searched_title = ""
            for word in searched_title:
                string_searched_title += word

            string_searched_topic = ""
            for word in searched_topic:
                string_searched_topic += word

            # For every search, the search details will be put in the table
            key_id = uuid.uuid1()
            sql = 'INSERT INTO database_search_info (id, searched_title, searched_topic) VALUE ("' + str(key_id.int) + '", "' + string_searched_title + '", "' + string_searched_topic +'")'
            cursor.execute(sql)
            connection.commit()

            # Put every article in the database table
            add_article(key_id)

            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)


def add_article(search_id):
    # Put every article in the database table
    for title in titles:
        # Every search found article should have a unique ID
        found_unique_id = None
        while found_unique_id == None:
            try:
                # Create ID
                id_voor_db = uuid.uuid1()
                # fill table
                sql = "INSERT INTO database_Search (id, article_id, key_id) " \
                      "VALUES ('" + str(id_voor_db.int) + "', '" + title.id + "', '" + str(search_id.int) + "')"
                cursor.execute(sql)

                # the connection is not autocommitted by default, so we must commit to save our changes
                connection.commit()
                # Unique ID is found, and article is put in db table
                found_unique_id = "gevonden"
            except:
                pass