from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.valladolid import JornadaValladolid, ValladolidPartido, ValladolidClub, CopaValladolid, PlayoffValladolid

valladolid_route_bp = Blueprint('valladolid_route_bp', __name__)

# LIGA REAL VALLADOLID
# Crear el calendario Real Valladolid
@valladolid_route_bp.route('/crear_calendario_valladolid', methods=['GET', 'POST'])
def ingresar_resultado_valladolid():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaValladolid(nombre=nombre_jornada)
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
            partido = ValladolidPartido(
                jornada_id=jornada.id,
                fecha=fecha,
                hora=hora,
                local=local,
                resultadoA=resultadoA,
                resultadoB=resultadoB,
                visitante=visitante,
                orden=i
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('valladolid_route_bp.calendarios_valladolid'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_valladolid.html')
# Ver calendario Real Valladolid en Admin
@valladolid_route_bp.route('/calendario_valladolid')
def calendarios_valladolid():
    jornadas = JornadaValladolid.query.order_by(JornadaValladolid.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(ValladolidPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(ValladolidPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_valladolid.html', jornadas=jornadas)
# Modificar jornada
@valladolid_route_bp.route('/modificar_jornada_valladolid/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_valladolid(id):
    jornada = db.session.query(JornadaValladolid).filter(JornadaValladolid.id == id).first()
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
                partido = db.session.query(ValladolidPartido).filter(ValladolidPartido.id == partido_id).first()
                if partido:
                    partido.hora = hora
                    partido.local = local
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.visitante = visitante                 
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('valladolid_route_bp.calendarios_valladolid'))
        # Si es un GET, pasamos la jornada con sus partidos ya cargados
        for partido in jornada.partidos:
            partido.hora = partido.hora.strftime('%H:%M') if partido.hora else ''
    return render_template('admin/calendarios/calend_valladolid.html', jornada=jornada)
# Eliminar jornada
@valladolid_route_bp.route('/eliminar_jornada_valladolid/<int:id>', methods=['GET','POST'])
def eliminar_jornada_valladolid(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaValladolid).filter(JornadaValladolid.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(ValladolidPartido).filter(ValladolidPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('valladolid_route_bp.calendarios_valladolid'))    
# Obtener datos Real Valladolid
def obtener_datos_valladolid():
    # Obtener todas las jornadas UEMC
    jornadas = JornadaValladolid.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(ValladolidPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(ValladolidPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Real Valladolid
@valladolid_route_bp.route('/equipos_futbol/calendario_valladolid')
def calendario_valladolid():
    datos = obtener_datos_valladolid()
    nuevos_datos_valladolid = [dato for dato in datos if dato]
    equipo_valladolid = 'Real Valladolid'
    tabla_partidos_valladolid = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el UEMC está jugando
            if equipo_local == equipo_valladolid or equipo_visitante == equipo_valladolid:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_valladolid:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_valladolid = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_valladolid:
                    tabla_partidos_valladolid[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_valladolid[equipo_contrario]:
                    tabla_partidos_valladolid[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_valladolid[equipo_contrario]:
                    tabla_partidos_valladolid[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_valladolid[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_valladolid[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_valladolid[equipo_contrario]['jornadas']:
                    tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_valladolid': rol_valladolid
                    }               
                # Asignamos los resultados según el rol del UEMC
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                    else:
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                else:
                    if not tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
                    else:
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_valladolid[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_valladolid
    return render_template('equipos_futbol/calendario_valladolid.html', tabla_partidos_valladolid=tabla_partidos_valladolid, nuevos_datos_valladolid=nuevos_datos_valladolid)
# Jornada 0 Real Valladolid
@valladolid_route_bp.route('/jornada0_valladolid', methods=['GET', 'POST'])
def jornada0_valladolid():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = ValladolidClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('valladolid_route_bp.jornada0_valladolid'))
    clubs = ValladolidClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_valladolid.html', clubs=clubs)
# Eliminar clubs jornada 0
@valladolid_route_bp.route('/eliminar_club_valladolid/<int:club_id>', methods=['POST'])
def eliminar_club_valladolid(club_id):
    club = ValladolidClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('valladolid_route_bp.jornada0_valladolid'))
# Crear la clasificación Real Valladolid
def generar_clasificacion_analisis_futbol_valladolid(data):
    clasificacion = defaultdict(lambda: {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'puntos': 0})
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
                clasificacion[equipo_local]['puntos'] += 3
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 3
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['empatados'] += 1          
            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1
            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante
            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local
            clasificacion[equipo_local]['diferencia_goles'] += resultado_local - resultado_visitante
            clasificacion[equipo_visitante]['diferencia_goles'] += resultado_visitante - resultado_local  
    clasificacion_ordenada = sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)
    return [{'equipo': equipo, 'datos': datos} for equipo, datos in clasificacion_ordenada]
# Ruta para mostrar la clasificación y análisis del UEMC
@valladolid_route_bp.route('/equipos_futbol/clasif_analisis_valladolid')
def clasif_analisis_valladolid():
    data = obtener_datos_valladolid()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_valladolid = generar_clasificacion_analisis_futbol_valladolid(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_valladolid = ValladolidClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_valladolid:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_valladolid):
            equipo = {
                'equipo': club.nombre,
                'datos': {
                    'puntos': 0,
                    'jugados': 0,
                    'ganados': 0,
                    'empatados': 0,
                    'perdidos': 0,
                    'favor': 0,
                    'contra': 0,
                    'diferencia_goles': 0
                }
            }
            clasificacion_analisis_valladolid.append(equipo)
    return render_template('equipos_futbol/clasif_analisis_valladolid.html',
        clasificacion_analisis_valladolid=clasificacion_analisis_valladolid)

# COPA DEL REY REAL VALLADOLID
# Creación de las eliminatorias de copa
@valladolid_route_bp.route('/crear_copa_valladolid', methods=['GET', 'POST'])
def crear_copa_valladolid():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')
        max_partidos = {
            'ronda1': 55,
            'ronda2': 28,
            'ronda3': 16,
            'octavos': 8,
            'cuartos': 4,
            'semifinales': 4,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos = int(request.form.get('num_partidos', '0').strip() or 0)
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaValladolid(
                eliminatoria=eliminatoria,
                fecha=request.form.get(f'fecha{i}', ''),
                hora=request.form.get(f'hora{i}', ''),
                local=request.form.get(f'local{i}', ''),
                resultadoA=request.form.get(f'resultadoA{i}', ''),
                resultadoB=request.form.get(f'resultadoB{i}', ''),
                visitante=request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('valladolid_route_bp.ver_copa_valladolid'))
    return render_template('admin/copa/copa_valladolid.html')   
# Ver las eliminatorias en Admin
@valladolid_route_bp.route('/copa_valladolid/')
def ver_copa_valladolid():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {
        e: CopaValladolid.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('admin/copa/copa_valladolid.html', datos_eliminatorias=datos_eliminatorias)
# Modificar las eliminatorias
@valladolid_route_bp.route('/modificar_copa_valladolid_post', methods=['POST'])
def modificar_copa_valladolid_post():
    eliminatoria = request.form['eliminatoria']
    num_partidos = int(request.form['num_partidos'])
    for i in range(num_partidos):
        partido_id = request.form.get(f'partido_id{i}')
        partido = CopaValladolid.query.get(partido_id)
        if partido:
            partido.eliminatoria = eliminatoria  # Opcional: si quieres actualizarla por partido
            partido.fecha = request.form.get(f'fecha{i}', '')
            partido.hora = request.form.get(f'hora{i}', '')
            partido.local = request.form.get(f'local{i}', '')
            partido.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido.visitante = request.form.get(f'visitante{i}', '')
    db.session.commit()
    return redirect(url_for('valladolid_route_bp.ver_copa_valladolid'))
# Eliminar las eliminatorias en Admin
@valladolid_route_bp.route('/eliminar_copa_valladolid/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_valladolid(eliminatoria):
    CopaValladolid.query.filter_by(eliminatoria=eliminatoria).delete()
    db.session.commit()
    return redirect(url_for('valladolid_route_bp.ver_copa_valladolid'))
# Ver las eliminatorias en la página principal Copa
@valladolid_route_bp.route('/valladolid_copa/')
def copas_valladolid():
    eliminatorias = ['ronda1', 'ronda2', 'ronda3', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_copa = {
        e: CopaValladolid.query.filter_by(eliminatoria=e).all()
        for e in eliminatorias
    }
    return render_template('copas/valladolid_copa.html', datos_copa=datos_copa)

# PLAYOFF ASCENSO REAL VALLADOLID
# Crear formulario para los playoff
@valladolid_route_bp.route('/crear_playoff_valladolid', methods=['GET', 'POST'])
def crear_playoff_valladolid():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'semifinales': 4,
            'final': 2
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffValladolid(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                resultadoA = request.form.get(f'resultadoA{i}', ''),
                resultadoB = request.form.get(f'resultadoB{i}', ''),
                visitante = request.form.get(f'visitante{i}', '')
            )
            PlayoffValladolid.query.filter_by(eliminatoria=eliminatoria).delete()
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('valladolid_route_bp.ver_playoff_valladolid'))
    return render_template('admin/playoffs/playoff_valladolid.html')
# Ver encuentros playoff en Admin
@valladolid_route_bp.route('/playoff_valladolid/')
def ver_playoff_valladolid():
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffValladolid.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffValladolid.orden).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_valladolid.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@valladolid_route_bp.route('/modificar_playoff_valladolid/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_valladolid(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffValladolid.query.get(int(partido_id))
            if not partido_obj:
                continue
            partido_obj.fecha = request.form.get(f'fecha{i}', '')
            partido_obj.hora = request.form.get(f'hora{i}', '')
            partido_obj.local = request.form.get(f'local{i}', '')
            partido_obj.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido_obj.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido_obj.visitante = request.form.get(f'visitante{i}', '')
            partido_obj.orden = i
        # Commit para guardar los cambios
        db.session.commit()
        flash('Playoff actualizado correctamente', 'success')
        return redirect(url_for('valladolid_route_bp.ver_playoff_valladolid'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('valladolid_route_bp.ver_playoff_valladolid'))
# Eliminar los partidos de los playoff
@valladolid_route_bp.route('/eliminar_playoff_valladolid/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_valladolid(eliminatoria):
    partidos = PlayoffValladolid.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('valladolid_route_bp.ver_playoff_valladolid'))
# Mostrar los playoffs del Real Valladolid
@valladolid_route_bp.route('/playoffs_valladolid/')
def playoffs_valladolid():
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffValladolid.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('playoff/valladolid_playoff.html', datos_playoff=datos_playoff)