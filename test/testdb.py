import flaskr
from flaskr import db
import configparser

if __name__ == '__main__':
    app = flaskr.create_app()
    config = configparser.ConfigParser()
    config.read(app.instance_path + "./application.cfg")
    args = [_ for _ in dict(config['MySql']).values()]
    db.get_db()
