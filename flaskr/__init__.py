#: AppFactor

import configparser
import os

from flask import (Flask)


def create_app(test_config=None):
    #: create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    #: 缺省值设置
    app.config.from_mapping(
        SECRET_KEY=os.urandom(16),
    )
    #: 测试与开发配置分离
    if test_config is None:
        app.config.from_pyfile('../config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    #: 实例文件创建
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    Strength_Configuration(app)

    from . import db
    def init_app(app):
        app.teardown_appcontext(db.close_connection)
        app.cli.add_command(db.init_db_command)

    init_app(app)

    from flaskr.view import auth
    app.register_blueprint(auth.bp)

    from flaskr.view import space
    app.register_blueprint(space.bp)

    from flaskr.view import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app


def Strength_Configuration(app):
    config = configparser.ConfigParser()
    config.read(app.instance_path + '/application.cfg')
    app.config.update(dict(config[app.config['DATABASE']]))
