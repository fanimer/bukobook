from flask import *
import pymysql
import configparser
from flaskr import app


def get_db():
    if 'db' not in g:
        info = current_app.config['DATABASE']
        g.db = pymysql.connect(
            info['HOST'], info['USERNAME'], info['PASSWORD'], info['DATABASE']
        )
        g.db.row_factory = pymysql.cursors.DictCursor
    return g.db


def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db(args)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read)
        db.commmit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(insert_sql, args=()):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(insert_sql, args)
        db.commit()
        return True
    except:
        db.rollback()
        return False
