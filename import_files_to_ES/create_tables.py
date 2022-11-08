import sqlite3
from sqlite3 import Error


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

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"/home/ubuntu/sqlite/project.db"

    sql_create_review_table = """ CREATE TABLE review (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    company_id INTEGER,
    reviewUnitId VARCHAR,
    review_title VARCHAR,
    review_text VARCHAR,
    experience_date DATE,
    publish_date DATE,
    rating INTEGER,
    isVerified VARCHAR,
    user_id VARCHAR,
    user_name VARCHAR,
    user_nbOfReviews INTEGER,
    user_country VARCHAR,
    response_company VARCHAR,
    response_company_date DATE,
    UNIQUE(reviewUnitId),
    UNIQUE(company_id, user_id),
    FOREIGN KEY (company_id) REFERENCES company (id)
    ); """

    sql_create_company_table = """CREATE TABLE company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    subSectorLevel1_id INTEGER,
    businessUnitId VARCHAR,
    website VARCHAR,
    display_name VARCHAR,
    score INTEGER,
    logoUrl VARCHAR,
    postal_address VARCHAR,
    postal_city VARCHAR,
    postal_zipCode VARCHAR,
    postal_country VARCHAR,
    contact_website VARCHAR,
    contact_email VARCHAR,
    contact_phone VARCHAR,
    reviews_resume VARCHAR,
    reviews_keywords VARCHAR,
    UNIQUE(businessUnitId),
    UNIQUE(website),
    UNIQUE(display_name),
    FOREIGN KEY (subSectorLevel1_id) REFERENCES subSectorLevel1 (id)
    );"""

    sql_create_subSector_table = """CREATE TABLE subSectorLevel1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    sector_id INTEGER,
    label_name VARCHAR,
    display_name VARCHAR,
    UNIQUE(label_name),
    UNIQUE(display_name),
    FOREIGN KEY (sector_id) REFERENCES sector (id)
    );"""

    sql_create_sector_table = """CREATE TABLE sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    label_name VARCHAR,
    display_name VARCHAR,
    UNIQUE(label_name),
    UNIQUE(display_name)
    );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create review table
        create_table(conn, sql_create_review_table)

        # create company table
        create_table(conn, sql_create_company_table)

        # create subSector table
        create_table(conn, sql_create_subSector_table)

        # create sector table
        create_table(conn, sql_create_sector_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()