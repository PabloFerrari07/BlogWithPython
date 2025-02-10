from flask import (
    #sirve para renderizar los templates de las vistas
    render_template,
    #sirve para registrar las vistas en la app
    Blueprint,
    #flash es para enviar mensajes de error o exito
    flash,
    #g es para almacenar informacion de la sesion
    g,
    #redirect es para redirigir a una vista
    redirect,
    #request es para obtener informacion de las peticiones
    request,
    #session es para almacenar informacion de la sesion
    session,
    #es para obtener la url de una vista
    url_for
)

from myBlog.Models.User import User
from werkzeug.security import check_password_hash, generate_password_hash
from myBlog import db
auth = Blueprint('auth', __name__, url_prefix='/auth')

#Registrar usuario
@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        userName = request.form.get('userName') #obtenemos el nombre de usuario
        password = request.form.get('password') #obtenemos la contraseña
        user = User(userName, generate_password_hash(password)) #creamos un objeto de tipo User

        error = None
        if not userName :
            error = 'se requiere nombre de usuario'
        elif not password:
            error = 'se requiere contraseña'

        userName = User.query.filter_by(userName=userName).first() #buscamos si el nombre de usuario ya existe

        if userName == None:
            db.session.add(user) #agregamos el usuario a la base de datos
            db.session.commit()
        else:
            error = f'el usuario {userName} ya existe'.format(userName)

        flash(error)
    return render_template('auth/register.html')

#Iniciar Sesion
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userName = request.form.get('userName') #obtenemos el nombre de usuario
        password = request.form.get('password') #obtenemos la contraseña

        error = None

        user = User.query.filter_by(userName=userName).first() #buscamos si el nombre de usuario ya existe

        if user == None:
           error = 'usuario incorrecto'
        elif not check_password_hash(user.password,password):
            error = 'contraseña incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            #return redirect(url_for('index.html'))
        flash(error)
    return render_template('auth/login.html')