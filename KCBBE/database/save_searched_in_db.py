from mysql.connector import connect, Error
from getpass import getpass
import uuid


def main_search(searched_topic, searched_title, titles):

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
            create_search_table_query = """
                                   CREATE TABLE IF NOT EXISTS database_Search(
                                   id VARCHAR (100),
                                   searched_titles VARCHAR (100),
                                   searched_topics VARCHAR (100),
                                   number_found_articles INTEGER,
                                   found_articles VARCHAR (100),
                                   PRIMARY KEY (id),
                                    FOREIGN KEY (found_articles) REFERENCES database_Information(id)
                                   )
                               """

            # Execute query to create table
            with connection.cursor() as cursor:
                cursor.execute(create_search_table_query)
                connection.commit()

            # get cursor object
            cursor = connection.cursor()

            # Make string of searched titles
            string_title = ""
            for item in searched_title:
                string_title += item + ", "
            print(string_title)

            # Make string of searched topics
            string_topic = ""
            for item in searched_topic:
                string_topic += item + ", "

            # If the id created is not in the db yet, insert the searched data into db
            # if the id is in the db a new one will be created, till there is one that is not in the db
            found_unique_id = None
            while found_unique_id is None:

                try:
                    id = uuid.uuid1()
                    print(id.int)

                    # fill table
                    sql = "INSERT INTO database_Search (id, searched_titles, searched_topics, number_found_articles) " \
                          "VALUES ('" + str(id.int) + "', '" + string_title + "', '" + string_topic + "', '" + str(len(titles)) + "')"
                    cursor.execute(sql)

                    # the connection is not autocommitted by default, so we must commit to save our changes
                    connection.commit()

                    # Data is added with a unique ID, so this step is done and found_unique_id should not be None anymore, otherwise it keeps looping
                    found_unique_id = "found a unique id, data is put in db"

                except:
                    pass

            # Query to create table if this one doesn't exists yet
            create_search_table_query = """
                    CREATE TABLE IF NOT EXISTS database_Article_search(
                    found_articles VARCHAR (500),
                    search_details VARCHAR (100),
                    FOREIGN KEY (found_articles) REFERENCES database_Information(id),
                    FOREIGN KEY (search_details) REFERENCES database_Search(id))
            """

            # Execute query to create table
            with connection.cursor() as cursor:
                cursor.execute(create_search_table_query)
                connection.commit()

            # get cursor object
            cursor = connection.cursor()

            # For every found article, the article id and search_deatials will be put in the database
            for article in titles:
                sql = 'INSERT INTO database_Article_search (found_articles, search_details) VALUES ("' + article.id + '", "' + str(id.int) + '")'
                cursor.execute(sql)
                connection.commit()

            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)