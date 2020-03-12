import flaskr
from flask import current_app, g
from flaskr import db
import configparser

if __name__ == '__main__':
    import subprocess

    print(subprocess.call("mysql -u root -q 123456 < schema.sql", shell=False))
