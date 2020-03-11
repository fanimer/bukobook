from flask import *
import pymysql
import configparser


class DdControl(object):
    @staticmethod
    def get_db(args=()):
        db = getattr(g, '_database', None)
        if db is None and args >= 4:
                db = g._database = pymysql.connect(args[0], args[1], args[2], args[3])
        return db

    @staticmethod
    def init_db(app):
        config = configparser.ConfigParser()
        config.read(app.instance_path + "./application.cfg")
        args = [_ for _ in dict(config['MySql']).values()]
        with app.app_context():
            db = get_db(args)
            with app.open_resource('schema.sql', mode='r') as f:
                db.cur