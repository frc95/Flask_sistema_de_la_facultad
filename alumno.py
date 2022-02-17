from flask import (
    Blueprint, render_template, request, flash, url_for, redirect, g
)
from app.auth import login_required_alumno

from app.db import get_db

bp = Blueprint('alumno', __name__, url_prefix="/alumno")

@bp.route('/materias', methods=['GET'])
@login_required_alumno
def listar_materias():
    db, c = get_db()
    c.execute(
        'SELECT m.*, u.nombre AS nombre_profesor, u.apellido , am.*'+
        'FROM materia AS m, alu_mat AS am, usuario AS u '+
        'WHERE am.id_alu = %s AND m.id = am.id_mat AND u.id = m.id_profesor'
        , (g.user['id'], )
    )
    materias = c.fetchall()
    return render_template('alumno/listas-materias.html', materias = materias)

@bp.route('/inscripcion-materia', methods=['GET', 'POST'])
@login_required_alumno
def inscripcion_materia():
    db, c = get_db()
    c.execute(
        'SELECT m.*, u.nombre AS nombre_profesor, u.apellido '+ 
        'FROM materia AS m, usuario AS u '+
        'WHERE m.id_profesor = u.id AND '+
        'NOT EXISTS (SELECT NULL FROM alu_mat AS am WHERE am.id_alu = %s AND am.id_mat = m.id)',
        (g.user['id'],)
    )
    allMaterias = c.fetchall()

    if request.method == 'POST':
            materiaid = request.form.get('materia')
            c.execute(
                'SELECT cupo FROM materia WHERE id = %s', (materiaid, )
            )
            row = c.fetchone()
            cupo = row['cupo']
            if cupo > 0:
                cupoFinal = cupo - 1
                c.execute(
                    'UPDATE materia SET cupo = %s WHERE id = %s', (cupoFinal, materiaid)
                )
                db.commit()

                c.execute('INSERT INTO alu_mat (id_alu, id_mat, nota_uno, nota_dos, promedio) VALUES (%s, %s, %s, %s, %s)', (g.user['id'], materiaid, 1, 1, 1))
                db.commit()

                return redirect(url_for('alumno.inscripcion_materia'))
            else:
                flash("No hay cupos")
            

    return render_template('alumno/inscripcion-materia.html', materias = allMaterias)