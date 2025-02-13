from flask import (
    render_template,
    Blueprint,
    flash,
    g,
    redirect,
    request,
    url_for
)


from werkzeug.exceptions import abort # Werkzeug is a WSGI utility library for Python
from myBlog.Models.Post import Post
from myBlog.Models.User import User
from myBlog.views.auth import login_required # importacion de login required
from myBlog import db


blog = Blueprint('blog', __name__) # Creacion de un Blueprint

#obtener un usuario
def get_user(id):
    user = User.query.get_or_404(id)
    return user


@blog.route('/')
def index():
    posts =Post.query.all()
    db.session.commit()
    return render_template('blog/index.html', posts=posts, get_user=get_user)

#Crear publicacion
@blog.route('/blog/create', methods=['GET','POST'])
@login_required #decorador para requerir login
def create():
    if request.method == 'POST':
        title = request.form.get('title') #obtenemos el nombre de usuario
        body = request.form.get('body') #obtenemos la contraseña
        post =Post(g.user.id,title,body) #creamos un objeto de tipo User

        error = None
        if not title :
            error = 'se requiere un titulo'

        if error is not None:
            flash(error)
        else:
            db.session.add(post) #agregamos el post a la base de datos
            db.session.commit()
            return redirect(url_for('blog.index'))



        flash(error)
    return render_template('blog/create.html')

#Update post
def get_post(id,check_autor=True):
    post = Post.query.get_or_404(id)

    if post is None:
        abort(404, f'Id {id} no existe.') #aborta la solicitud y muestra un mensaje de error

    if check_autor and post.autor != g.user.id:
        abort(404) #aborta la solicitud y muestra un mensaje de error
    return post


@blog.route('/blog/update/<int:id>', methods=['GET','POST'])
@login_required #decorador para requerir login
def update(id):
    post = get_post(id)


    if request.method == 'POST':
        post.title = request.form.get('title') #obtenemos el nombre de usuario
        post.body = request.form.get('body') #obtenemos la contraseña
  


        error = None
        if not post.title :
            error = 'se requiere un titulo'

        if error is not None:
            flash(error)
        else:
            db.session.add(post) #agregamos el post a la base de datos
            db.session.commit()
            return redirect(url_for('blog.index'))



        flash(error)
    return render_template('blog/update.html', post=post)

#Delete post
@blog.route('/blog/delete/<int:id>')
@login_required #decorador para requerir login
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('blog.index'))