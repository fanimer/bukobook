import flaskr
from flask import current_app, g
from flaskr import db
import configparser

if __name__ == '__main__':
    app = flaskr.create_app()
    with app.app_context():
        db.get_db()
