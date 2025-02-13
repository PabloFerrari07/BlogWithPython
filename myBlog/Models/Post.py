from myBlog import db
from datetime import datetime
class Post(db.Model):
    #nombre de las tablas
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    #relacion de 1 a muchos entre usuarios y posts
    autor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)

    #instancia de la clase
    def __init__(self, autor, title,body) -> None:
        self.autor = autor
        self.title = title
        self.body = body

    def __repr__(self) -> str:
        return f'Post {self.title}'