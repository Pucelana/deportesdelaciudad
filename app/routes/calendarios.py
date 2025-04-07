from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.calend import JornadaUEMC, UEMCPartido

calendario_bp = Blueprint('calendario_bp', __name__)

# EQUIPOS BALONCESTO
#Todo el proceso de calendario y clasificación del UEMC
# Ingresar los resultados de los partidos UEMC
@calendario_bp.route('/admin/crear_calendario_uemc', methods=['GET', 'POST'])
def ingresar_resultado_uemc():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaUEMC(nombre=nombre_jornada)
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')            
            # Validar y convertir la fecha
            fecha = convertir_fecha(fecha)
            # Validar y convertir la hora
            hora = convertir_hora(hora)
            # Crear el objeto partido y agregarlo a la sesión
            partido = UEMCPartido(
                jornada_id=jornada.id,
                fecha=fecha,
                hora=hora,
                local=local,
                resultadoA=resultadoA,
                resultadoB=resultadoB,
                visitante=visitante
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('calendario_bp.calendarios_uemc'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('/admin/calendarios/calend_uemc.html')

def convertir_fecha(fecha_str):
    """Convierte una fecha en formato dd.mm.yy a yyyy-mm-dd"""
    if fecha_str and fecha_str != "0.00.00":
        try:
            # Convertir la fecha usando el formato dd.mm.yy
            return datetime.strptime(fecha_str, "%d.%m.%y").date()  # Retorna como un objeto DATE
        except ValueError:
            # Si el formato no es válido, retorna None
            return None
    return None  # Si la fecha está vacía o es inválida, retorna None

def convertir_hora(hora_str):
    """Convierte una hora en formato hh:mm a un objeto TIME"""
    if hora_str and hora_str != "00:00":
        try:
            # Convertir la hora usando el formato hh:mm
            return datetime.strptime(hora_str, "%H:%M").time()  # Retorna como un objeto TIME
        except ValueError:
            # Si el formato no es válido, retorna None
            return None
    return None  # Si la hora está vacía o es inválida, retorna None

# Ver calendario UEMC en Admin
@calendario_bp.route('/admin/calendario_uemc')
def calendarios_uemc():
    # Consulta todas las jornadas y sus partidos relacionados
    jornadas = JornadaUEMC.query.order_by(JornadaUEMC.id.desc()).all()
    # SQLAlchemy ya tiene relación configurada, puedes acceder con jornada.partidos directamente
    return render_template('/admin/calendarios/calend_uemc.html', jornadas=jornadas)

@calendario_bp.route('/modificar_jornada_uemc/<int:id>', methods=['POST'])
def modificar_jornada_uemc(id):
    # Obtener los datos del formulario
    nombre_jornada = request.form['nombre']
    num_partidos = int(request.form['num_partidos'])    
    # Modificar la jornada
    jornada = db.session.query(JornadaUEMC).filter(JornadaUEMC.id == id).first()
    if jornada:
        jornada.nombre = nombre_jornada        
    # Actualizar los partidos asociados a la jornada
    for i in range(num_partidos):
        partido_id = request.form[f'partido_id{i}']
        fecha = request.form[f'fecha{i}']
        hora = request.form[f'hora{i}']
        local = request.form[f'local{i}']
        resultadoA = request.form[f'resultadoA{i}']
        resultadoB = request.form[f'resultadoB{i}']
        visitante = request.form[f'visitante{i}']        
        # Buscar el partido y actualizarlo
        partido = db.session.query(UEMCPartido).filter(UEMCPartido.id == partido_id).first()
        if partido:
            partido.fecha = convertir_fecha(fecha)
            partido.hora = convertir_hora(hora)
            partido.local = local
            partido.resultadoA = resultadoA
            partido.resultadoB = resultadoB
            partido.visitante = visitante   
    # Confirmar todos los cambios en la base de datos
    db.session.commit()
    # Redirigir al calendario después de modificar la jornada
    return redirect(url_for('calendarios_uemc'))
@calendario_bp.route('/eliminar_jornada_uemc/<int:id>', methods=['POST'])
def eliminar_jornada_uemc(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaUEMC).filter(JornadaUEMC.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(UEMCPartido).filter(UEMCPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('calendarios_uemc'))