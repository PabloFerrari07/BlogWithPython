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

auth = Blueprint('auth', __name__, url_prefix='/auth')

#Registrar usuario
@auth.route('/register', methods=['GET', 'POST'])
def register():
    return "registrar usuario"