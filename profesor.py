from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, current_app, g
)
from app.auth import login_required_profesor

from app.db import get_db

bp = Blueprint('profesor', __name__, url_prefix="/profesor")

@bp.route('/materias', methods=['GET', 'POST'])
@login_required_profesor
def listar_materias():
    db, c = get_db()
    c.execute(
        'SELECT * FROM materia WHERE id_profesor = %s', (g.user['id'], )
    )
    allMaterias = c.fetchall()

    if request.method == 'POST':
        materiaid = request.form.get('materia')
        c.execute(
            'SELECT u.*, am.* FROM usuario AS u, alu_mat AS am WHERE am.id_mat = %s AND u.id = id_alu', (materiaid,)
        )
        alumnos = c.fetchall()

        if alumnos:
            return render_template('profesor/listar-materias.html', materias = allMaterias, alumnos = alumnos)
        else:
            flash('No hay alumnos en la materia seleccionada. Espere hasta que un alumno se inscriba', 'info')

    return render_template('profesor/listar-materias.html', materias = allMaterias)

@bp.route('<int:id_alumno>/modificar-notas', methods=['GET', 'POST'])
@login_required_profesor
def modificar_notas(id_alumno):
    nota_uno = request.args.get('nota_uno')
    nota_dos = request.args.get('nota_dos')
    id_mat = request.args.get('id_mat')

    if request.method == 'POST':
        formNota1 = request.form.get('nota_uno')
        formNota2 = request.form.get('nota_dos')
        promedio = (int(formNota1) + int(formNota2)) / 2

        db, c = get_db()
        c.execute(
            'UPDATE alu_mat SET nota_uno = %s, nota_dos = %s, promedio = %s WHERE id_alu = %s AND id_mat = %s', (formNota1, formNota2, promedio, id_alumno, id_mat)
        )
        db.commit()

        return redirect(url_for('profesor.listar_materias'))


    return render_template('profesor/modificar-nota.html', nota_uno = nota_uno, nota_dos = nota_dos)