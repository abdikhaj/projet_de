import sqlite3
from sqlite3 import Error

db_path = "/home/utilisateur/Documents/datascientest/projet_data/projet_de/es_to_sqlite/project.db"


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

def main():
    database = r"{}".format(db_path)

    ##############################################
    # permanent tables
    sql_create_review_table = """ CREATE TABLE IF NOT EXISTS review (
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
    FOREIGN KEY (company_id) REFERENCES company (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    ); """

    sql_create_review_index1 = """
    CREATE UNIQUE INDEX IF NOT EXISTS rev_index1
    ON review(company_id, user_id);
    """

    sql_create_review_index2 = """
    CREATE UNIQUE INDEX IF NOT EXISTS rev_index2
    ON review(reviewUnitId);
    """

    sql_create_company_table = """CREATE TABLE IF NOT EXISTS company (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
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
    UNIQUE(website)
    );"""

    sql_create_company_index1 = """
    CREATE UNIQUE INDEX IF NOT EXISTS comp_index1
    ON company(businessUnitId);
    """

    sql_create_company_index2 = """
    CREATE UNIQUE INDEX IF NOT EXISTS comp_index2
    ON company(display_name);
    """

    sql_create_sectors_table = """CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    parent_label_name VARCHAR,
    parent_display_name VARCHAR,
    child_label_name VARCHAR,
    child_display_name VARCHAR,
    subchild_label_name VARCHAR,
    subchild_display_name VARCHAR
    );"""

    sql_create_sectors_index1 = """
    CREATE UNIQUE INDEX IF NOT EXISTS sectors_index1
    ON sectors(parent_label_name, child_label_name, subchild_label_name);
    """

    sql_create_link_company_sectors = """CREATE TABLE IF NOT EXISTS link_company_sectors (
    lastupdated_date TIMESTAMP default current_timestamp,
    company_id INTEGER,
    sectors_id INTEGER,
    FOREIGN KEY (sectors_id) REFERENCES sectors (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );"""

    sql_create_link_company_sectors_index1 = """
    CREATE UNIQUE INDEX IF NOT EXISTS link_company_sectors_index1
    ON link_company_sectors(company_id, sectors_id);
    """
    

    sql_create_resume_table = """CREATE TABLE IF NOT EXISTS review_resume (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    company_id INTEGER,
    resume_type VARCHAR,
    resume_text VARCHAR,
    resume_keywords VARCHAR,
    FOREIGN KEY (company_id) REFERENCES company (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );"""

    sql_create_resume_index1 = """
    CREATE UNIQUE INDEX IF NOT EXISTS resume_index1
    ON review_resume(company_id, resume_type);
    """

    ############################################################
    # temporary tables
    sql_temp_create_review_table = """ CREATE TABLE IF NOT EXISTS ztemp_review (
    lastupdated_date TIMESTAMP default current_timestamp,
    businessUnitId VARCHAR,
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
    response_company_date DATE
    ); """

    sql_temp_create_company_table = """CREATE TABLE IF NOT EXISTS ztemp_company (
    lastupdated_date TIMESTAMP default current_timestamp,
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
    contact_phone VARCHAR
    );"""

    sql_temp_create_sectors_table = """CREATE TABLE IF NOT EXISTS ztemp_sectors (
    lastupdated_date TIMESTAMP default current_timestamp,
    parent_label_name VARCHAR,
    parent_display_name VARCHAR,
    child_label_name VARCHAR,
    child_display_name VARCHAR,
    subchild_label_name VARCHAR,
    subchild_display_name VARCHAR
    );"""

    sql_temp_create_lk_company_sectors_table = """CREATE TABLE IF NOT EXISTS ztemp_lk_company_sectors (
    lastupdated_date TIMESTAMP default current_timestamp,
    company_businessUnitId VARCHAR,
    subchild_label_name VARCHAR
    );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        ############################
        # create permanent tables
        create_object(conn, sql_create_review_table)
        create_object(conn, sql_create_company_table)
        create_object(conn, sql_create_sectors_table)
        create_object(conn, sql_create_link_company_sectors)
        create_object(conn, sql_create_resume_table)

        ###############################
        # create index
        create_object(conn, sql_create_review_index1)
        create_object(conn, sql_create_review_index2)

        create_object(conn, sql_create_company_index1)
        create_object(conn, sql_create_company_index2)

        create_object(conn, sql_create_sectors_index1)
        create_object(conn, sql_create_link_company_sectors_index1)

        create_object(conn, sql_create_resume_index1)

        ###############################
        # create temp tables
        create_object(conn, sql_temp_create_review_table)
        create_object(conn, sql_temp_create_company_table)
        create_object(conn, sql_temp_create_sectors_table)
        create_object(conn, sql_temp_create_lk_company_sectors_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()