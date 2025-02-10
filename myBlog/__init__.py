from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

#cargar
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
