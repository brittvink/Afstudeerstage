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

def add_word_to_db(onder, woord):
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
            create_information_table_query = """
                        CREATE TABLE IF NOT EXISTS database_Vocabulair(
                        id VARCHAR(100),
                        key_id VARCHAR (100),
                        word VARCHAR(100),
                        PRIMARY KEY (id))
            """

            # Execute query to create table
            cursor.execute(create_information_table_query)
            connection.commit()

            id = uuid.uuid1()
            id_num = id.int

            sql = "INSERT INTO database_Vocabulair (id, key_id, word) VALUES ('" + str(id_num) + "', '" + onder + "', '" + woord + "')"
            cursor.execute(sql)
            connection.commit()

            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)