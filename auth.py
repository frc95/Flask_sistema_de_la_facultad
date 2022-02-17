import functools
from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app, session, g
)
from werkzeug.security import check_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix="/auth")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        errors = []

        if not email:
            errors.append('El email es obligatorio')
        if not password:
            errors.append('La contraseña es obligatorio')

        if len(errors) == 0:
            db , c = get_db()
            c.execute(
            'SELECT * FROM usuario WHERE email = %s', (email, )
            )
            user = c.fetchone()

            if user is None:
                errors.append('Usuario y o contraseña invalida')
            elif not check_password_hash(user['password'], password):
                errors.append('Usuario y o contraseña invalida')

            if len(errors) == 0:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('usuario.index'))
            else:
                for error in errors:
                    flash(error)

        else:
            for error in errors:
                flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from usuario where id = %s', (user_id,)
        )
        g.user = c.fetchone()

def login_required_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        elif g.user['type'] == 'Administrador':
            return view(**kwargs)
        
        else:
            return redirect(url_for('usuario.index'))
    
    return wrapped_view

def login_required_profesor(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        elif g.user['type'] == 'Profesor':
            return view(**kwargs)
        
        else:
            return redirect(url_for('usuario.index'))
    
    return wrapped_view

def login_required_alumno(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        elif g.user['type'] == 'Alumno':
            return view(**kwargs)
        
        else:
            return redirect(url_for('usuario.index'))
    
    return wrapped_view


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('usuario.index'))


def verificar_email(email):
    validar = True

    db, c = get_db()
    c.execute('SELECT email FROM usuario WHERE email = %s', (email, ))
    row = c.fetchone()

    if not row:
        validar = False
    else:
        pass

    return validar