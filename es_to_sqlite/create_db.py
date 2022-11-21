import sqlite3
from sqlite3 import Error


db_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/es_to_sqlite/project.db"

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

create_connection("{db_path}".format(db_path=db_path))
