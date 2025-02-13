from myBlog import db

class User(db.Model):
    #nombre de las tablas
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(80))
    password = db.Column(db.Text)

    #instancia de la clase
    def __init__(self, userName, password) -> None:
        self.userName = userName
        self.password = password

    def __repr__(self) -> str:
        return f'User {self.userName}'