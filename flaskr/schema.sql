DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY auto_increment,
    username varchar(18) UNIQUE NOT NULL,
    password TEXT NOT NULL
    );

CREATE TABLE post (
    id INTEGER PRIMARY KEY auto_increment,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user(id)
    );

CREATE TABLE comment (
    id INTEGER PRIMARY KEY auto_increment,
    reviewer_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL,
    reply_to INTEGER,
    by_reply VARCHAR(18),
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    body TEXT NOT NULL,
    FOREIGN KEY (reviewer_id) REFERENCES user(id),
    FOREIGN KEY (post_id) REFERENCES post(id),
    FOREIGN KEY (by_reply) REFERENCES user(username),
    FOREIGN KEY (reply_to) REFERENCES comment(id)
    );

