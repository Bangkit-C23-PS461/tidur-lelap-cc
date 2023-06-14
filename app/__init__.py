from flask import Flask
import configparser
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os


#================================================= OTHER CONFIG ==========================================================
config = configparser.RawConfigParser()
base_path = os.getcwd()

conf_file = '{base_path}/config.ini'.format(base_path=base_path)
config.read(conf_file)

app = Flask(__name__)

app.config['SECRET_KEY'] = config['APP']['SECRET_KEY']
app.config['JWT_SECRET_KEY'] = config['APP']['SECRET_KEY']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=7)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
# app.config['SQLALCHEMY_DATABASE_URI'] = config['SQL']['SQL_URI'] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes