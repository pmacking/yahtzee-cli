"""
This module controls creation of SQLite3 db, players and scores table, and
insertion of data.
"""

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """
    Creates connection to SQLite database specified by db_file.
    :param db_file: db path as string.
    :return: Connection object.
    """
    connection = None

    try:
        connection = sqlite3.connect(db_file)
        print("Connection to SQLite DB successful.")
    except Error as e:
        print(f"The error '{e}' occurred.")

    return connection


def execute_query(connection, query):
    """ Execute an SQL query from the query statement.
    :param connection: Connection object.
    :param query: An SQL query.
    :return: None
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
    except Error as e:
        print(f"The error '{e}' occurred.")


def create_sqlite_database():
    """Main function to create SQLite db in data/; player, and score tables.
    """
    # TODO: update database path after testing to ./data/db_sqlite3.db
    database = "./sqlite3_db.db"

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );"""

    sql_create_games_table = """
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_created TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );"""

    sql_create_users_games_table = """
    CREATE TABLE IF NOT EXISTS users_games_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        ones INTEGER NOT NULL,
        twos INTEGER NOT NULL,
        threes INTEGER NOT NULL,
        fours INTEGER NOT NULL,
        fives INTEGER NOT NULL,
        sixes INTEGER NOT NULL,
        three_of_a_kind INTEGER NOT NULL,
        four_of_a_kind INTEGER NOT NULL,
        full_house INTEGER NOT NULL,
        small_straight INTEGER NOT NULL,
        large_straight INTEGER NOT NULL,
        yahtzee INTEGER NOT NULL,
        chance INTEGER NOT NULL,
        yahtzee_bonus INTEGER NOT NULL,
        top_score INTEGER NOT NULL,
        top_bonus_score INTEGER NOT NULL,
        top_bonus_score_delta INTEGER NOT NULL,
        total_top_score INTEGER NOT NULL,
        total_bottom_score INTEGER NOT NULL,
        grand_total_score INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
        FOREIGN KEY (game_id) REFERENCES games (id)
    );"""

    connection = create_connection(database)

    # if connection is established create the tables
    if connection is not None:
        # create users table
        execute_query(connection, sql_create_users_table)

        # create games table
        execute_query(connection, sql_create_games_table)

        # create users_game_data table
        execute_query(connection, sql_create_users_games_table)
    else:
        print("Error, cannot create the database connection.")

    connection.close()


create_sqlite_database()
