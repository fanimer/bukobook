from flask import *
import pymysql
import configparser


def get_db(args=()):
    db = getattr(g, '_database', None)
    if db is None and args >= 4:
        db = g._database = pymysql.connect(args[0], args[1], args[2], args[3])
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db(app):
    config = configparser.ConfigParser()
    config.read(app.instance_path + "./application.cfg")
    args = [_ for _ in dict(config['MySql']).values()]
    with app.app_context():
        db = get_db(args)
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read)
        db.commmit()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return dict((cur.description[idx][0], value)
                for idx, value in enumerate(rv)) if one else rv


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
