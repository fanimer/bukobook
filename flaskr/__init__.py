#: AppFactor

import os
from flask import *
import configparser

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

    #: 测试用发布页
    @app.route('/index')
    def index():
        return render_template('blog/index.html')

    @app.route('/')
    def home():
        return "hello, world"

    from . import db
    def init_app(app):
        app.teardown_appcontext(db.close_connection)
        app.cli.add_command(db.init_db_command)

    init_app(app)

    return app


def Strength_Configuration(app):
    config = configparser.ConfigParser()
    app.from_mapping(config.read(app.instance_path + 'application.cfg'))
    print(app.config["Host"])
