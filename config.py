import os

#: 各目录路径配置
environ = os.environ
PROJECT_PATH = os.path.dirname(__file__)
APP_PATH = os.path.join(PROJECT_PATH, "flaskr")
TEMPLATE_FOLDER = os.path.join(APP_PATH, "templates")
STATIC_FOLDER = os.path.join(APP_PATH, "static")
DEBUG = True

#: 上传配置
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'sql'}

#: MySql配置

#:
DOWNLOAD_FOLDER = '/tmp'
HOME_PATH = '/'

#:
HOST = '0.0.0.0'
PORT = 5000
