from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC

uemc_route_bp = Blueprint('uemc_route_bp', __name__)

# EQUIPOS BALONCESTO
#Todo el proceso de calendario y clasificación del UEMC
# Ingresar los resultados de los partidos UEMC
@uemc_route_bp.route('/crear_calendario_uemc', methods=['GET', 'POST'])
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
        return redirect(url_for('uemc_route_bp.calendarios_uemc'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_uemc.html')
def convertir_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None
def convertir_hora(hora_str):
    try:
        return datetime.strptime(hora_str, "%H:%M").time()
    except (ValueError, TypeError):
        return None
# Ver calendario UEMC en Admin
@uemc_route_bp.route('/calendario_uemc')
def calendarios_uemc():
    jornadas = JornadaUEMC.query.order_by(JornadaUEMC.id.asc()).all()
    return render_template('admin/calendarios/calend_uemc.html', jornadas=jornadas)
# Modificar jornada
@uemc_route_bp.route('/modificar_jornada_uemc/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_uemc(id):
    jornada = db.session.query(JornadaUEMC).filter(JornadaUEMC.id == id).first()
    
    if jornada:
        if request.method == 'POST':
            nombre_jornada = request.form['nombre']
            num_partidos = int(request.form['num_partidos'])
            jornada.nombre = nombre_jornada  # Actualizar el nombre de la jornada
            
            # Actualizar los partidos
            for i in range(num_partidos):
                partido_id = request.form[f'partido_id{i}']
                fecha = request.form[f'fecha{i}']
                hora = request.form[f'hora{i}']
                local = request.form[f'local{i}']
                resultadoA = request.form[f'resultadoA{i}']
                resultadoB = request.form[f'resultadoB{i}']
                visitante = request.form[f'visitante{i}']
                
                # Obtener el partido correspondiente por ID
                partido = db.session.query(UEMCPartido).filter(UEMCPartido.id == partido_id).first()
                
                if partido:
                    partido.fecha = convertir_fecha(fecha)
                    partido.hora = convertir_hora(hora)
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante

            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('uemc_route_bp.calendarios_uemc'))

        # Si es un GET, pasamos la jornada con sus partidos ya cargados
        for partido in jornada.partidos:
            partido.fecha = partido.fecha.strftime('%Y-%m-%d') if partido.fecha else ''
            partido.hora = partido.hora.strftime('%H:%M') if partido.hora else ''
        
    return render_template('admin/calendarios/calend_uemc.html', jornada=jornada)
# Eliminar jornada
@uemc_route_bp.route('/eliminar_jornada_uemc/<int:id>', methods=['GET','POST'])
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
    return redirect(url_for('uemc_route_bp.calendarios_uemc'))
# Obtener datos UEMC
def obtener_datos_uemc():
    # Obtener todas las jornadas UEMC
    jornadas = JornadaUEMC.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = UEMCPartido.query.filter_by(jornada_id=jornada.id).all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario UEMC
@uemc_route_bp.route('/equipos_basket/calendario_uemc')
def calendario_uemc():
    datos = obtener_datos_uemc()
    nuevos_datos_uemc = [dato for dato in datos if dato]
    equipo_uemc = 'UEMC Real Valladolid'
    tabla_partidos_uemc = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_uemc or equipo_visitante == equipo_uemc:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_uemc:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_uemc = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_uemc:
                    tabla_partidos_uemc[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_uemc[equipo_contrario]:
                    tabla_partidos_uemc[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_uemc[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_uemc[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_uemc[equipo_contrario]['jornadas']:
                    tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_uemc': rol_uemc
                    }               
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                    else:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                else:
                    if not tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
                    else:
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_uemc[equipo_contrario]['jornadas'][jornada['nombre']]['rol_uemc'] = rol_uemc
    return render_template('equipos_basket/calendario_uemc.html', tabla_partidos_uemc=tabla_partidos_uemc, nuevos_datos_uemc=nuevos_datos_uemc)
# Jornada 0 UEMC
@uemc_route_bp.route('/jornada0_uemc', methods=['GET', 'POST'])
def jornada0_uemc():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = UEMCClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('uemc_route_bp.jornada0_uemc'))
    clubs = UEMCClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_uemc.html', clubs=clubs)
# Eliminar clubs jornada 0
@uemc_route_bp.route('/eliminar_club_uemc/<int:club_id>', methods=['POST'])
def eliminar_club_uemc(club_id):
    club = UEMCClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('uemc_route_bp.jornada0_uemc'))
# Crear la clasificación UEMC
def generar_clasificacion_analisis_baloncesto_uemc(data):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_canastas': 0, 'puntos': 0})
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido.local 
            equipo_visitante = partido.visitante   
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB 
            if resultado_local is None or resultado_visitante is None:
                print(f"Partido sin resultados válidos: {partido}")
                continue            
            try:
                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1           
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_canastas'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_canastas'] += resultado_visitante - resultado_local  
    clasificacion_ordenada = sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_canastas']), reverse=True)
    return [{'equipo': equipo, 'datos': datos} for equipo, datos in clasificacion_ordenada]
# Ruta para mostrar la clasificación y análisis del UEMC
@uemc_route_bp.route('/equipos_basket/clasif_analisis_uemc')
def clasif_analisis_uemc():
    data = obtener_datos_uemc()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_uemc = generar_clasificacion_analisis_baloncesto_uemc(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_uemc = UEMCClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_uemc:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_uemc):
            equipo = {
                'equipo': club.nombre,
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_canastas': 0
                }
            }
            clasificacion_analisis_uemc.append(equipo)
    return render_template('equipos_basket/clasif_analisis_uemc.html',
        clasificacion_analisis_uemc=clasificacion_analisis_uemc)
# COPA UEMC
 