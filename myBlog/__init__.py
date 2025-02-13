from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cargar las configuraciones
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)

# Importar vistas
from myBlog.views.auth import auth
app.register_blueprint(auth)

from myBlog.views.blog import blog
app.register_blueprint(blog)

# Crear la base de datos dentro del contexto de la aplicación
with app.app_context():
    db.create_all()
