from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.aliados import JornadaAliados, AliadosPartido, AliadosClub, PlayoffAliados, CopaAliados, SupercopaAliados

aliados_route_bp = Blueprint('aliados_route_bp', __name__)

# LIGA BSR FUNDACIÓN ALIADOS
#Todo el proceso de calendario y clasificación del ALIADOS
# Ingresar los resultados de los partidos ALIADOS
@aliados_route_bp.route('/crear_calendario_aliados', methods=['GET', 'POST'])
def ingresar_resultado_aliados():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaAliados(nombre=nombre_jornada)
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
            # Crear el objeto partido y agregarlo a la sesión
            partido = AliadosPartido(
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
        return redirect(url_for('aliados_route_bp.calendarios_aliados'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_aliados.html')
# Ver calendario Ponce en Admin
@aliados_route_bp.route('/calendario_aliados')
def calendarios_aliados():
    jornadas = JornadaAliados.query.order_by(JornadaAliados.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(AliadosPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(AliadosPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_ponce.html', jornadas=jornadas)
# Modificar jornada
@aliados_route_bp.route('/modificar_jornada_aliados/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_aliados(id):
    jornada = db.session.query(JornadaAliados).filter(JornadaAliados.id == id).first()
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
                partido = db.session.query(AliadosPartido).filter(AliadosPartido.id == partido_id).first()
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('aliados_route_bp.calendarios_aliados'))        
    return render_template('admin/calendarios/calend_aliados.html', jornada=jornada)
# Eliminar jornada
@aliados_route_bp.route('/eliminar_jornada_aliados/<int:id>', methods=['GET','POST'])
def eliminar_jornada_aliados(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaAliados).filter(JornadaAliados.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(AliadosPartido).filter(AliadosPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('aliados_route_bp.calendarios_aliados'))
# Obtener datos Aliados
def obtener_datos_aliados():
    # Obtener todas las jornadas Aliados
    jornadas = JornadaAliados.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = AliadosPartido.query.filter_by(jornada_id=jornada.id).all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Aliados
@aliados_route_bp.route('/equipos_basket/calendario_aliados')
def calendario_aliados():
    datos = obtener_datos_aliados()
    nuevos_datos_aliados = [dato for dato in datos if dato]
    equipo_aliados = 'Fundación Aliados'
    tabla_partidos_aliados = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Ponce está jugando
            if equipo_local == equipo_aliados or equipo_visitante == equipo_aliados:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_aliados:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aliados = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aliados = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_aliados:
                    tabla_partidos_aliados[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_aliados[equipo_contrario]:
                    tabla_partidos_aliados[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aliados[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_aliados[equipo_contrario]:
                    tabla_partidos_aliados[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aliados[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_aliados[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_aliados[equipo_contrario]['jornadas']:
                    tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_aliados': rol_aliados
                    }               
                # Asignamos los resultados según el rol del Aliados
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                    else:
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                else:
                    if not tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
                    else:
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aliados[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aliados'] = rol_aliados
    return render_template('equipos_basket/calendario_aliados.html', tabla_partidos_aliados=tabla_partidos_aliados, nuevos_datos_aliados=nuevos_datos_aliados)
# Jornada 0 Aliados
@aliados_route_bp.route('/jornada0_aliados', methods=['GET', 'POST'])
def jornada0_aliados():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = AliadosClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('aliados_route_bp.jornada0_aliados'))
    clubs = AliadosClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_aliados.html', clubs=clubs)
# Eliminar clubs jornada 0
@aliados_route_bp.route('/eliminar_club_aliados/<int:club_id>', methods=['POST'])
def eliminar_club_aliados(club_id):
    club = AliadosClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('aliados_route_bp.jornada0_aliados'))
# Crear la clasificación Ponce
def generar_clasificacion_analisis_baloncesto_aliados(data):
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
@aliados_route_bp.route('/equipos_basket/clasif_analisis_aliados')
def clasif_analisis_aliados():
    data = obtener_datos_aliados()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_aliados = generar_clasificacion_analisis_baloncesto_aliados(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_aliados = AliadosClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_aliados:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_aliados):
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
            clasificacion_analisis_aliados.append(equipo)
    return render_template('equipos_basket/clasif_analisis_aliados.html',
        clasificacion_analisis_aliados=clasificacion_analisis_aliados)
    