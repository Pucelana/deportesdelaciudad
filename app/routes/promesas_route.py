from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.promesas import JornadaPromesas, PromesasPartido, PromesasClub, PlayoffPromesas

promesas_route_bp = Blueprint('promesas_route_bp', __name__)

# LIGA REAL VALLADOLID PROMESAS
# Crear el calendario Real Valladolid Promesas
@promesas_route_bp.route('/crear_calendario_promesas', methods=['GET', 'POST'])
def ingresar_resultado_promesas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaPromesas(nombre=nombre_jornada)
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
            partido = PromesasPartido(
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
        return redirect(url_for('promesas_route_bp.calendarios_promesas'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_promesas.html')
# Ver calendario Real Valladolid Promesas en Admin
@promesas_route_bp.route('/calendario_promesas')
def calendarios_promesas():
    jornadas = JornadaPromesas.query.order_by(JornadaPromesas.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(PromesasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(PromesasPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_promesas.html', jornadas=jornadas)
# Modificar jornada
@promesas_route_bp.route('/modificar_jornada_promesas/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_promesas(id):
    jornada = db.session.query(JornadaPromesas).filter(JornadaPromesas.id == id).first()
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
                partido = db.session.query(PromesasPartido).filter(PromesasPartido.id == partido_id).first()
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
            return redirect(url_for('promesas_route_bp.calendarios_promesas'))
        # Si es un GET, pasamos la jornada con sus partidos ya cargados
        for partido in jornada.partidos:
            partido.hora = partido.hora.strftime('%H:%M') if partido.hora else ''
    return render_template('admin/calendarios/calend_promesas.html', jornada=jornada)
# Eliminar jornada
@promesas_route_bp.route('/eliminar_jornada_promesas/<int:id>', methods=['GET','POST'])
def eliminar_jornada_promesas(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaPromesas).filter(JornadaPromesas.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(PromesasPartido).filter(PromesasPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('promesas_route_bp.calendarios_promesas'))    
# Obtener datos Real Valladolid Promesas
def obtener_datos_promesas():
    # Obtener todas las jornadas Promesas
    jornadas = JornadaPromesas.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(PromesasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(PromesasPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Real Valladolid Promesas
@promesas_route_bp.route('/equipos_futbol/calendario_promesas')
def calendario_promesas():
    datos = obtener_datos_promesas()
    nuevos_datos_promesas = [dato for dato in datos if dato]
    equipo_promesas = 'RV Promesas'
    tabla_partidos_promesas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Promesas está jugando
            if equipo_local == equipo_promesas or equipo_visitante == equipo_promesas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_promesas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_promesas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_promesas = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_promesas:
                    tabla_partidos_promesas[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_promesas[equipo_contrario]:
                    tabla_partidos_promesas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_promesas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_promesas[equipo_contrario]:
                    tabla_partidos_promesas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_promesas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_promesas[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_promesas[equipo_contrario]['jornadas']:
                    tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_promesas': rol_promesas                    }               
                # Asignamos los resultados según el rol del Promesas
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_promesas
                    else:
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_promesas
                else:
                    if not tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_promesas
                    else:
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_promesas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_valladolid'] = rol_promesas
    return render_template('equipos_futbol/calendario_promesas.html', tabla_partidos_promesas=tabla_partidos_promesas, nuevos_datos_promesas=nuevos_datos_promesas)
# Jornada 0 Real Valladolid Promesas
@promesas_route_bp.route('/jornada0_promesas', methods=['GET', 'POST'])
def jornada0_promesas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = PromesasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('promesas_route_bp.jornada0_promesas'))
    clubs = PromesasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_promesas.html', clubs=clubs)
# Eliminar clubs jornada 0
@promesas_route_bp.route('/eliminar_club_promesas/<int:club_id>', methods=['POST'])
def eliminar_club_promesas(club_id):
    club = PromesasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('promesas_route_bp.jornada0_promesas'))
# Crear la clasificación Real Valladolid Promesas
def generar_clasificacion_analisis_futbol_promesas(data):
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
# Ruta para mostrar la clasificación y análisis del Promesas
@promesas_route_bp.route('/equipos_futbol/clasif_analisis_promesas')
def clasif_analisis_promesas():
    data = obtener_datos_promesas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_promesas = generar_clasificacion_analisis_futbol_promesas(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_promesas = PromesasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_promesas:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_promesas):
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
            clasificacion_analisis_promesas.append(equipo)
    return render_template('equipos_futbol/clasif_analisis_promesas.html',
        clasificacion_analisis_promesas=clasificacion_analisis_promesas)

# PLAYOFF ASCENSO REAL VALLADOLID PROMESAS
# Crear formulario para los playoff
@promesas_route_bp.route('/crear_playoff_promesas', methods=['GET', 'POST'])
def crear_playoff_promesas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'semifinales': 20,
            'final': 10
        }.get(eliminatoria, 0)

        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0

        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"

        # 🧹 Eliminar partidos ANTES de agregar nuevos
        PlayoffPromesas.query.filter_by(eliminatoria=eliminatoria).delete()

        for i in range(num_partidos):
            partido = PlayoffPromesas(
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
        return redirect(url_for('promesas_route_bp.ver_playoff_promesas'))

    return render_template('admin/playoffs/playoff_promesas.html')
# Ver encuentros playoff en Admin
@promesas_route_bp.route('/playoff_promesas/')
def ver_playoff_promesas():
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffPromesas.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffPromesas.orden).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_promesas.html', datos_playoff=datos_playoff)
# Modificar los partidos de los playoff
@promesas_route_bp.route('/modificar_playoff_promesas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_promesas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffPromesas.query.get(int(partido_id))
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
        return redirect(url_for('promesas_route_bp.ver_playoff_promesas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('promesas_route_bp.ver_playoff_promesas'))
# Eliminar los partidos de los playoff
@promesas_route_bp.route('/eliminar_playoff_promesas/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_promesas(eliminatoria):
    partidos = PlayoffPromesas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('promesas_route_bp.ver_playoff_promesas'))
# Mostrar los playoffs del Real Valladolid Promesas
@promesas_route_bp.route('/playoffs_promesas/')
def playoffs_promesas():
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffPromesas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos
    return render_template('playoff/promesas_playoff.html', datos_playoff=datos_playoff)    