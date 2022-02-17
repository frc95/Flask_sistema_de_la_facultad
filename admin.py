from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app
)
from werkzeug.security import generate_password_hash
from app.auth import login_required_admin, verificar_email

from app.db import get_db

bp = Blueprint('admin', __name__, url_prefix="/admin")


@bp.route('/alta', methods=['GET', 'POST'])
@login_required_admin
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        errors = []

        if not email:
            errors.append('El email es obligatorio')
        if not password:
            errors.append('La contraseña es obligatorio')
        if not nombre:
            errors.append('El nombre es obligatorio')
        if not apellido:
            errors.append('El apellido es obligatorio')
        
        if verificar_email(email):
            errors.append('Este email ya esta asociado a otra cuenta')
        
        if len(errors) == 0:
            db, c = get_db()
            c.execute('INSERT INTO usuario (nombre, apellido, email, password, type) VALUES (%s, %s, %s, %s, %s)', (nombre, apellido ,email, generate_password_hash(password), "Administrador"))
            db.commit()

            return redirect(url_for('usuario.index'))
        else:
            for error in errors:
                flash(error)
        

    return render_template('admin/alta.html')

@bp.route('/alta-materia', methods=['GET', 'POST'])
@login_required_admin
def create_materia():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        cuatrimestre = request.form.get('cuatrimestre')
        cupo = request.form.get('cupo')
        anio = request.form.get('anio')
        turno = request.form.get('turno')
        id_profesor = request.form.get('profesor')
        errors = []

        if not nombre:
            errors.append('El nombre es obligatorio')
        if not cupo:
            errors.append('El cupo es obligatorio')
        if not anio:
            errors.append('El año es obligatorio')
        if len(errors) == 0:
            db, c = get_db()
            c.execute('INSERT INTO materia (nombre, cuatrimestre, cupo, anio, turno, id_profesor) VALUES (%s, %s, %s, %s, %s, %s)', (nombre, cuatrimestre, cupo, anio, turno, id_profesor))
            db.commit()

            return redirect(url_for('usuario.index'))
        else:
            for error in errors:
                flash(error)
        

    db, c = get_db()
    c.execute(
        'SELECT * FROM usuario WHERE type = %s', ("Profesor",)
    )
    profesores = c.fetchall()
    return render_template('admin/alta-materia.html', profesores = profesores)



@bp.route('/listado-materias', methods=['GET', 'POST'])
@login_required_admin
def listado_materias():
    db, c = get_db()
    c.execute(
        'SELECT m.*, u.nombre AS nombre_profesor, u.apellido FROM materia AS m INNER JOIN usuario AS u ON m.id_profesor = u.id'
    )
    allMaterias = c.fetchall()

    if request.method == 'POST':
        materiaid = request.form.get('materia')
        c.execute(
            'SELECT u.*, am.* FROM usuario AS u, alu_mat AS am WHERE am.id_mat = %s AND u.id = id_alu', (materiaid,)
        )
        alumnos = c.fetchall()
        return render_template('admin/listado-materias.html', materias = allMaterias, alumnos = alumnos)


    return render_template('admin/listado-materias.html', materias = allMaterias)

@bp.route('/listado-usuarios', methods=['GET', 'POST'])
@login_required_admin
def listado_usuarios():
    db, c = get_db()
    c.execute(
        'SELECT * FROM usuario'
    )
    usuarios = c.fetchall()

    if request.method == 'POST':
        tipo = request.form.get('tipo')
        c.execute(
            'SELECT * FROM usuario WHERE type like %s', ('%'+tipo+'%',)
        )
        usuarios = c.fetchall()
        return render_template('admin/listado-usuarios.html', usuarios = usuarios)

    return render_template('admin/listado-usuarios.html', usuarios = usuarios)


@bp.route('/<int:id_usuario>/eliminar-usuario', methods=['GET', 'POST'])
@login_required_admin
def eliminar_usuario(id_usuario):
    db, c = get_db()
    tipo = request.args.get('tipo')

    if tipo == 'Alumno':
        c.execute('DELETE FROM alu_mat WHERE id_alu = %s', (id_usuario,))
        db.commit()
    elif tipo == 'Profesor':

        c.execute('SELECT id FROM materia WHERE id_profesor = %s', (id_usuario,))
        materias = c.fetchall()

        for materia in materias:
            c.execute('DELETE FROM alu_mat WHERE id_mat = %s', (materia['id'],))
            db.commit()
        
        c.execute('DELETE FROM materia WHERE id_profesor = %s', (id_usuario,))
        db.commit()

        
    c.execute('DELETE FROM usuario where id = %s', (id_usuario,))
    db.commit()
    return redirect(url_for('admin.listado_usuarios'))

@bp.route('/<int:id_usuario>/editar-usuario', methods=['GET', 'POST'])
@login_required_admin
def editar_usuario(id_usuario):

    if request.method == 'POST':
        nombreForm = request.form.get('nombre')
        apellidoForm = request.form.get('apellido')
        emailForm = request.form.get('email')

        db, c = get_db()
        c.execute(
            'UPDATE usuario SET nombre = %s, apellido = %s, email = %s WHERE id = %s', (nombreForm, apellidoForm, emailForm, id_usuario)
        )
        db.commit()

        return redirect(url_for('admin.listado_usuarios'))

    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    email = request.args.get('email')

    return render_template('admin/editar-usuario.html', nombre = nombre, apellido = apellido, email = email)