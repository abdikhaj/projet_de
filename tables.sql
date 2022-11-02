'''
les tables : 
user
reviews
company
sub_sector
sector


'''

CREATE TABLE user (
 id INTEGER NOT NULL, 
 firstname VARCHAR,
 lastname VARCHAR,
 user_country VARCHAR,
 PRIMARY KEY (id) );


CREATE TABLE review (
    id INTEGER NOT NULL, 
    title VARCHAR,
    review_text VARCHAR,
    review_date DATE,
    score INTEGER,
    response_company VARCHAR,
    user_id INTEGER,
    PRIMARY KEY (id), 
    FOREIGN KEY (user_id) REFERENCES user (id));



CREATE TABLE company (
    id INTEGER NOT NULL, 
    Company_name VARCHAR,
    Company_country VARCHAR,
    Company_score INTEGER,
    review_id INTEGER,
    PRIMARY KEY (id), 
    FOREIGN KEY (review_id) REFERENCES review (id));


CREATE TABLE sub_sector (
    id INTEGER NOT NULL, 
    sub_sector_name VARCHAR,
    company_id INTEGER,
    sector_id INTEGER,
    PRIMARY KEY (id), 
    FOREIGN KEY (sector_id) REFERENCES sector (id)
    FOREIGN KEY (company_id) REFERENCES company (id));

CREATE TABLE sector (
    id INTEGER NOT NULL, 
    sector VARCHAR,
    PRIMARY KEY (id));



