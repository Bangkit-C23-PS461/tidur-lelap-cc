from flask import Flask
import configparser
from flask_sqlalchemy import SQLAlchemy

#================================================= OTHER CONFIG ==========================================================
config = configparser.RawConfigParser()
base_path = "" # Need to add absolute path

conf_file = base_path+'config.ini'
config.read(conf_file)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e8be6c76f90f01893eedc58ee07c65fcc1e4339b1a854dc1edc9969402a84bc2'
app.config['SQLALCHEMY_DATABASE_URI'] = config['SQL']['SQL_URI'] 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes