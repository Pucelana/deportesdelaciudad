from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from ..models.horario import Horario

resultados_bp = Blueprint('resultados', __name__)

# Página principal: muestra todos los resultados
@resultados_bp.route('/')
def sitio_home():
    resultados = Horario.query.all()
    return render_template('index.html', resultados=resultados)
# Página de administración: muestra los marcadores
@resultados_bp.route('/admin/pub_marcadores')
def pub_marcadores():
    resultados_publicados = Horario.query.all()
    return render_template('admin/pub_marcadores.html', resultados_publicados=resultados_publicados)
# Crear nuevos resultados
@resultados_bp.route('/admin/crear_resultados', methods=['GET', 'POST'])
def crear_resultado():
    if request.method == 'POST':
        nuevo_resultado = Horario(
            seccion=request.form.get('seccion', ''),
            liga=request.form.get('liga', ''),
            equipoA=request.form.get('equipoA', ''),
            resultado1=request.form.get('resultado1', ''),
            equipoB=request.form.get('equipoB', ''),
            resultado2=request.form.get('resultado2', ''),
            fecha_partido=request.form.get('fecha_parti', '')
        )
        db.session.add(nuevo_resultado)
        db.session.commit()
        return redirect(url_for('resultados.pub_marcadores'))
    return render_template('admin/crear_resultados.html')
# Modificar marcador existente
@resultados_bp.route('/modificar_marcador/<int:id>', methods=['POST'])
def modificar_marcador(id):
    resultado = Horario.query.get_or_404(id)
    resultado.seccion = request.form.get('seccion')
    resultado.liga = request.form.get('liga')
    resultado.equipoA = request.form.get('equipoA')
    resultado.resultado1 = request.form.get('resultado1')
    resultado.equipoB = request.form.get('equipoB')
    resultado.resultado2 = request.form.get('resultado2')
    resultado.fecha_partido = request.form.get('fecha_parti')
    db.session.commit()
    return redirect(url_for('resultados.pub_marcadores'))
# Eliminar marcador
@resultados_bp.route('/eliminar_resultado/<int:id>', methods=['POST'])
def eliminar_resultado(id):
    resultado = Horario.query.get_or_404(id)
    db.session.delete(resultado)
    db.session.commit()
    return redirect(url_for('resultados.pub_marcadores'))