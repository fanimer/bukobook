import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from flaskr import create_app, db

app = create_app()
manager = Manager(app)

manager.add_command("runserver", Server())

if __name__ == '__main__':
    manager.run()
