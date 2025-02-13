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

import functools

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
            return redirect(url_for('auth.login'))
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
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('auth/login.html')


@auth.before_app_request #se ejecuta antes de cualquier peticion
def load_logged_in_user():
    user_id = session.get('user_id') #obtenemos el id del usuario
    if user_id is None: #si no hay un usuario logeado
        g.user = None #g.user es igual a None
    else:
        g.user = User.query.get_or_404(user_id) #g.user es igual al usuario con el id user_id

    
@auth.route('/logout')
def logout():
    session.clear() #limpiamos la sesion
    return redirect(url_for('blog.index')) #redirigimos a la vista index.html


def login_required(view):
    @functools.wraps(view) #decorador para que la funcion view tenga los mismos atributos que la funcion original
    def wrapped_view(**kwargs):
        if g.user is None: #si no hay un usuario logeado
            return redirect(url_for('auth.login'))
        return view(**kwargs) #retornamos la funcion view

    return wrapped_view  #retornamos la funcion wrapped_view