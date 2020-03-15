import click
import pymysql
from flask import (g, current_app)
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            current_app.config['host'],
            current_app.config['user'],
            current_app.config['pwd'],
            current_app.config['db'],
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()
    with current_app.open_resource('schema.sql') as f:
        string = f.read().decode('utf8')
    query = string.split(';')[:-1]
    query = [_.replace('\r', '') for _ in query]
    query = [_.replace('\n', '') + ';' for _ in query]
    for _ in query:
        cur.execute(_)
    db.commit()
    cur.close()


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database')


def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv


def insert_db(insert_sql: str, args=()):
    db = get_db()
    cur = db.cursor()
    cur.execute(insert_sql, args)
    try:
        db.commit()
        cur.close()
        return True
    except:
        db.rollback()
        cur.close()
        return False

