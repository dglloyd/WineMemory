from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.bcrypt import Bcrypt
import psycopg2

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import views, models
