from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app
)
from app.auth import verificar_email

from app.db import get_db

from werkzeug.security import generate_password_hash

bp = Blueprint('usuario', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    return render_template('usuarios/index.html')

@bp.route('/alta', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        type = request.form.get('type')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        errors = []

        if not email:
            errors.append('El email es obligatorio')
        if not password:
            errors.append('La contraseña es obligatorio')
        if not type:
            errors.append('El tipo es obligatorio')
        if not nombre:
            errors.append('El nombre es obligatorio')
        if not apellido:
            errors.append('El apellido es obligatorio')

        if verificar_email(email):
            errors.append('Este email ya esta asociado a otra cuenta')
        
        if len(errors) == 0:
            db, c = get_db()
            c.execute('INSERT INTO usuario (nombre, apellido, email, password, type) VALUES (%s, %s, %s, %s, %s)', (nombre, apellido, email, generate_password_hash(password), type))
            db.commit()

            return redirect(url_for('usuario.index'))
        else:
            for error in errors:
                flash(error)

    return render_template('usuarios/alta.html')




