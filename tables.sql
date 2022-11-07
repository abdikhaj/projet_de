'''
les tables : 
user
reviews
company
sub_sector
sector

'''
CREATE TABLE review (
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
    PRIMARY KEY (id), 
    FOREIGN KEY (company_id) REFERENCES company (id));



CREATE TABLE company (
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
    PRIMARY KEY (id), 
    FOREIGN KEY (subSectorLevel1_id) REFERENCES subSectorLevel1 (id));


CREATE TABLE subSectorLevel1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    sector_id INTEGER,
    label_name VARCHAR,
    display_name VARCHAR,
    UNIQUE(label_name),
    UNIQUE(display_name),
    PRIMARY KEY (id), 
    FOREIGN KEY (sector_id) REFERENCES sector (id));

CREATE TABLE sector (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lastupdated_date TIMESTAMP default current_timestamp,
    label_name VARCHAR,
    display_name VARCHAR,
    UNIQUE(label_name),
    UNIQUE(display_name),
    PRIMARY KEY (id));



