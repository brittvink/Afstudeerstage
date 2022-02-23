def main_stoppen():
    alles = []
    import pandas as pd
    import argparse
    from getpass import getpass
    from mysql.connector import connect, Error

    # Read input file
    df = pd.read_csv("out.txt")

    # Try to make a connection with the database
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
            with connection.cursor() as cursor:
                cursor.execute(create_information_table_query)
                connection.commit()

            # get cursor object
            cursor = connection.cursor()

            # creating column list for insertion
            cols = "`,`".join([str(i) for i in df.columns.tolist()])

            # Insert DataFrame records one by one if they are not in the database present yet.
            for i, row in df.iterrows():
                sql = "INSERT INTO `database_Information` (`" + cols + "`) VALUES (" + "%s," * (
                        len(row) - 1) + "%s) ON DUPLICATE KEY UPDATE id=id"
                cursor.execute(sql, tuple(row))

                # the connection is not autocommitted by default, so we must commit to save our changes
                connection.commit()

            cursor.execute("SELECT * FROM database_Information")
            alles = cursor.fetchall()

            # Close connection
            cursor.close()
            connection.close()

    # Throw error if trying to connect fails
    except Error as e:
        print(e)

    return alles