import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
DATABASE_DIR = BASEDIR + '/database/'

DATABASE_PATH = DATABASE_DIR + 'data.sqlite'

DIR_LIST = [DATABASE_DIR]

for directory in DIR_LIST:
    if not os.path.isdir(directory):
        os.mkdir(directory)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
