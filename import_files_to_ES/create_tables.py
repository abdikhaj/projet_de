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
    database = r"/home/ubuntu/sqlite/project.db"

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
    CREATE UNIQUE INDEX rev_index1
    ON review(company_id, user_id);
    """

    sql_create_review_index2 = """
    CREATE UNIQUE INDEX rev_index2
    ON review(reviewUnitId);
    """

    sql_create_company_table = """CREATE TABLE IF NOT EXISTS company (
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
    UNIQUE(website),
    FOREIGN KEY (subSectorLevel1_id) REFERENCES subSectorLevel1 (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );"""

    sql_create_company_index1 = """
    CREATE UNIQUE INDEX comp_index1
    ON company(businessUnitId);
    """

    sql_create_company_index2 = """
    CREATE UNIQUE INDEX comp_index2
    ON company(display_name);
    """

    sql_create_subSector_table = """CREATE TABLE IF NOT EXISTS subSectorLevel1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    sector_id INTEGER,
    label_name VARCHAR,
    display_name VARCHAR,
    FOREIGN KEY (sector_id) REFERENCES sector (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
    );"""

    sql_create_subSector_index1 = """
    CREATE UNIQUE INDEX subS_index1
    ON subSectorLevel1(label_name);
    """

    sql_create_subSector_index2 = """
    CREATE UNIQUE INDEX subS_index2
    ON subSectorLevel1(display_name);
    """

    sql_create_sector_table = """CREATE TABLE IF NOT EXISTS sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    label_name VARCHAR,
    display_name VARCHAR
    );"""

    sql_create_sector_index1 = """
    CREATE UNIQUE INDEX sector_index1
    ON sector(label_name);
    """

    sql_create_sector_index2 = """
    CREATE UNIQUE INDEX sector_index2
    ON sector(display_name);
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
    CREATE UNIQUE INDEX resume_index1
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
    subSector1_label_name VARCHAR,
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

    sql_temp_create_subSector_table = """CREATE TABLE IF NOT EXISTS ztemp_subSectorLevel1 (
    lastupdated_date TIMESTAMP default current_timestamp,
    sector_label_name VARCHAR,
    label_name VARCHAR,
    display_name VARCHAR
    );"""

    sql_temp_create_sector_table = """CREATE TABLE IF NOT EXISTS ztemp_sector (
    lastupdated_date TIMESTAMP default current_timestamp,
    label_name VARCHAR,
    display_name VARCHAR
    );"""


    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        ############################
        # create review table
        create_object(conn, sql_create_review_table)

        # create company table
        create_object(conn, sql_create_company_table)

        # create subSector table
        create_object(conn, sql_create_subSector_table)

        # create sector table
        create_object(conn, sql_create_sector_table)

        # create resume table
        create_object(conn, sql_create_resume_table)

        ###############################

        # create index
        create_object(conn, sql_create_review_index1)
        create_object(conn, sql_create_review_index2)

        create_object(conn, sql_create_company_index1)
        create_object(conn, sql_create_company_index2)

        create_object(conn, sql_create_subSector_index1)
        create_object(conn, sql_create_subSector_index2)

        create_object(conn, sql_create_sector_index1)
        create_object(conn, sql_create_sector_index2)

        create_object(conn, sql_create_resume_index1)

        ###############################
        # create temp review table
        create_object(conn, sql_temp_create_review_table)

        # create temp company table
        create_object(conn, sql_temp_create_company_table)

        # create temp subSector table
        create_object(conn, sql_temp_create_subSector_table)

        # create temp sector table
        create_object(conn, sql_temp_create_sector_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()