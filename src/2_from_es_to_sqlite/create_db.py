import sqlite3
from sqlite3 import Error
from custom_vars_db import db_path

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

create_connection("{db_path}".format(db_path=db_path()))
