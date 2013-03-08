from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.debug = True
db = SQLAlchemy(app)
mail = Mail(app)

from app import views, models