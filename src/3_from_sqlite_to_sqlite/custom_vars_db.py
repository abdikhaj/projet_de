import sqlite3
from sqlite3 import Error

def db_path():
    return "/home/utilisateur/Documents/datascientest/projet_data/projet_de/src/2_from_es_to_sqlite/project.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

def create_object(conn, create_table_sql):
    """ create a table or index from the create_table|index_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE|INDEX statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_data_temp(conn, insert_sql, list_to_insert):
    """ insert data from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        c = conn.cursor()
        c.executemany(insert_sql, list_to_insert)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

def insert_data_perm(conn, insert_sql):
    """ insert data from the insert_sql statement
    :param conn: Connection object
    :param insert_sql: a INSERT INTO statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(insert_sql)
        conn.commit()
        return c.lastrowid
    except Error as e:
        print(e)

def delete_data(conn, delete_sql):
    """ delete data from the delete_sql statement
    :param conn: Connection object
    :param delete_sql: a DELETE FROM statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(delete_sql)
        conn.commit()
    except Error as e:
        print(e)