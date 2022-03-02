from mysql.connector import connect, Error
from getpass import getpass
import uuid


def main_search(searched_topic, searched_title, titles):

    try:
        with connect(
                host="localhost",
                user="root",
                password="HoiAap12",
                database="KCBBE2",

        ) as connection:
            # Print connection
            print(connection)

            # Query to create table if this one doesn't exists yet
            create_search_table_query = """
                                   CREATE TABLE IF NOT EXISTS database_search(
                                   id VARCHAR (100),
                                   key_id VARCHAR (100),
                                   article_id VARCHAR (100),
                                   PRIMARY KEY (id))
                               """

            # Execute query to create table
            with connection.cursor() as cursor:
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
            with connection.cursor() as cursor:
                cursor.execute(create_search_table_query)
                connection.commit()

            # get cursor object
            cursor = connection.cursor()

            # If the id created is not in the db yet, insert the searched data into db
            # if the id is in the db a new one will be created, till there is one that is not in the db

            string_searched_title = ""
            for word in searched_title:
                string_searched_title += word

            string_searched_topic = ""
            for word in searched_topic:
                string_searched_topic += word


            # For every found article, the article id and search_deatials will be put in the database
            key_id = uuid.uuid1()
            sql = 'INSERT INTO database_search_info (id, searched_title, searched_topic) VALUE ("' + str(key_id.int) + '", "' + string_searched_title + '", "' + string_searched_topic +'")'
            cursor.execute(sql)
            connection.commit()


            for title in titles:
                found_unique_id = None
                while found_unique_id == None :
                    try:
                        id_voor_db = uuid.uuid1()
                        # fill table
                        sql = "INSERT INTO database_Search (id, article_id, key_id) " \
                                      "VALUES ('" + str(id_voor_db.int) + "', '" + title.id +  "', '" + str(key_id.int) + "')"
                        cursor.execute(sql)

                        # the connection is not autocommitted by default, so we must commit to save our changes
                        connection.commit()
                        found_unique_id = "gevonden"
                    except:
                        pass


            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)