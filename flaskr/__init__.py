import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
DATABASE_DIR = BASEDIR + '/database/'

DATABASE_PATH = DATABASE_DIR + 'data.sqlite'

DIR_LIST = [DATABASE_DIR]

for directory in DIR_LIST:
    if not os.path.isdir(directory):
        os.mkdir(directory)

app = Flask(__name__, static_url_path='', static_folder='{}/dist'.format(BASEDIR))

app.config['SECRET_KEY'] = 'development' if app.config['DEBUG'] else os.urandom(256)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = ''

db = SQLAlchemy(app)
