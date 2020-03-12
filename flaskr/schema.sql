DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY auto_increment,
    username varchar(18) UNIQUE NOT NULL,
    password varchar(18) NOT NULL
    );

CREATE TABLE post (
    id INTEGER PRIMARY KEY auto_increment,
    authod_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title text NOT NULL,
    body text NOT NULL,
    FOREIGN KEY (authod_id) REFERENCES user (id)
);

