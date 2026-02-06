from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.panteras import JornadaPanteras, PanterasPartido, PanterasClub, PlayoffPanteras, CopaPanteras, SupercopaPanteras, EuropaPanteras, Clasificacion

panteras_route_bp = Blueprint('panteras_route_bp', __name__)

# LIGA CPLV MUNIA PANTERAS
# Crear el calendario CPLV Munia Panteras
@panteras_route_bp.route('/crear_calendario_panteras', methods=['GET', 'POST'])
def ingresar_resultado_panteras():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaPanteras(nombre=nombre_jornada)
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonusA = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonusB = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')            
            # Crear el objeto partido y agregarlo a la sesión
            partido = PanterasPartido(
                jornada_id=jornada.id,
                fecha=fecha,
                hora=hora,
                local=local,
                bonusA = bonusA,
                resultadoA=resultadoA,
                resultadoB=resultadoB,
                bonusB = bonusB,
                visitante=visitante,
                orden=i
            )
            db.session.add(partido)
        # Confirmar todos los cambios en la base de datos
        db.session.commit()
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('panteras_route_bp.calendarios_panteras'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_panteras.html')
# Ver calendario CPLV Panteras en Admin
@panteras_route_bp.route('/calendario_panteras')
def calendarios_panteras():
    jornadas = JornadaPanteras.query.order_by(JornadaPanteras.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(PanterasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(PanterasPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_panteras.html', jornadas=jornadas)
# Modificar jornada
@panteras_route_bp.route('/modificar_jornada_panteras/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_panteras(id):
    jornada = db.session.query(JornadaPanteras).filter(JornadaPanteras.id == id).first()
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
                bonusA = request.form[f'bonusA{i}']
                resultadoA = request.form[f'resultadoA{i}']
                resultadoB = request.form[f'resultadoB{i}']
                bonusB = request.form[f'bonusB{i}']
                visitante = request.form[f'visitante{i}']                
                # Obtener el partido correspondiente por ID
                partido = db.session.query(PanterasPartido).filter(PanterasPartido.id == partido_id).first()
                if partido:
                    partido.fecha = fecha
                    partido.hora = hora
                    partido.local = local
                    partido.bonusA = bonusA
                    partido.resultadoA = resultadoA
                    partido.resultadoB = resultadoB
                    partido.bonusB = bonusB
                    partido.visitante = visitante                 
                    orden = int(request.form.get(f'orden{i}', i))  # Usa 'i' como fallback
                    partido.orden = orden
            # Guardar cambios en la base de datos
            db.session.commit()
            return redirect(url_for('panteras_route_bp.calendarios_panteras'))
    return render_template('admin/calendarios/calend_panteras.html', jornada=jornada)
# Eliminar jornada
@panteras_route_bp.route('/eliminar_jornada_panteras/<int:id>', methods=['GET','POST'])
def eliminar_jornada_panteras(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaPanteras).filter(JornadaPanteras.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(PanterasPartido).filter(PanterasPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('panteras_route_bp.calendarios_panteras'))    
# Obtener datos CPLV Panteras
def obtener_datos_panteras():
    # Obtener todas las jornadas CPLV Panteras
    jornadas = JornadaPanteras.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(PanterasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(PanterasPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario CPLV Panteras
@panteras_route_bp.route('/equipos_hockey/calendario_panteras')
def calendario_panteras():
    datos = obtener_datos_panteras()
    nuevos_datos_panteras = [dato for dato in datos if dato]
    equipo_panteras = 'Panteras Caja Rural'
    tabla_partidos_panteras = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_panteras or equipo_visitante == equipo_panteras:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_panteras:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_panteras = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_panteras = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_panteras:
                    tabla_partidos_panteras[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_panteras[equipo_contrario]:
                    tabla_partidos_panteras[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_panteras[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_panteras[equipo_contrario]:
                    tabla_partidos_panteras[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_panteras[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_panteras[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_panteras[equipo_contrario]['jornadas']:
                    tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_panteras': rol_panteras
                    }               
                # Asignamos los resultados según el rol del CPLV Munia Panteras
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                    else:
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                else:
                    if not tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
                    else:
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_panteras[equipo_contrario]['jornadas'][jornada['nombre']]['rol_panteras'] = rol_panteras
    return render_template('equipos_hockey/calendario_panteras.html', tabla_partidos_panteras=tabla_partidos_panteras, nuevos_datos_panteras=nuevos_datos_panteras)
# Jornada 0 CPLV Munia Panteras
@panteras_route_bp.route('/jornada0_panteras', methods=['GET', 'POST'])
def jornada0_panteras():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = PanterasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('panteras_route_bp.jornada0_panteras'))
    clubs = PanterasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_panteras.html', clubs=clubs)
# Eliminar clubs jornada 0
@panteras_route_bp.route('/eliminar_club_panteras/<int:club_id>', methods=['POST'])
def eliminar_club_panteras(club_id):
    club = PanterasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('panteras_route_bp.jornada0_panteras'))
# Crear la clasificación CPLV Munia Panteras
def generar_clasificacion_analisis_hockey_panteras(data):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0 })
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido.local 
            equipo_visitante = partido.visitante
            bonus_local = partido.bonusA   
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB 
            bonus_visitante = partido.bonusB
            if resultado_local in(None, '', ' ' ) or resultado_visitante in (None, '', ' '):
                print(f"Partido sin resultados válidos: {partido}")
                continue             
            try:
                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)
                bonus_local = int(bonus_local or 0)
                bonus_visitante = int(bonus_visitante or 0)
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
                clasificacion[equipo_local]['puntos'] += 1 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 1 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1 
            clasificacion[equipo_local]['bonus'] += bonus_local
            clasificacion[equipo_visitante]['bonus'] += bonus_visitante              
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
# Ruta para mostrar la clasificación y análisis del CPLV Munia Panteras
@panteras_route_bp.route('/equipos_hockey/clasif_analisis_panteras')
def clasif_analisis_panteras():
    data = obtener_datos_panteras()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_panteras = generar_clasificacion_analisis_hockey_panteras(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_panteras = PanterasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_panteras:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_panteras):
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
                    'diferencia_goles': 0,
                    'bonus': 0
                }
            }
            clasificacion_analisis_panteras.append(equipo)
    return render_template('equipos_hockey/clasif_analisis_panteras.html',
        clasificacion_analisis_panteras=clasificacion_analisis_panteras)

# PLAYOFF CPLV MUNIA PANTERAS
# Crear formulario para los playoff
@panteras_route_bp.route('/crear_playoff_panteras', methods=['GET', 'POST'])
def crear_playoff_panteras():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'play-out': 3,
            'semifinales': 3,
            'final': 3
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffPanteras(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                resultadoA = request.form.get(f'resultadoA{i}', ''),
                resultadoB = request.form.get(f'resultadoB{i}', ''),
                visitante = request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('panteras_route_bp.ver_playoff_panteras'))
    return render_template('admin/playoffs/playoff_panteras.html')
# Ver encuentros playoff en Admin
@panteras_route_bp.route('/playoff_panteras/')
def ver_playoff_panteras():
    eliminatorias = ['play-out' ,'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffPanteras.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffPanteras.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_panteras.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@panteras_route_bp.route('/modificar_playoff_panteras/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_panteras(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffPanteras.query.get(int(partido_id))
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
        return redirect(url_for('panteras_route_bp.ver_playoff_panteras'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('panteras_route_bp.ver_playoff_panteras'))
# Eliminar los partidos de los playoff
@panteras_route_bp.route('/eliminar_playoff_panteras/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_panteras(eliminatoria):
    partidos = PlayoffPanteras.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('panteras_route_bp.ver_playoff_panteras'))
# Mostrar los playoffs del CPLV Munia Panteras
@panteras_route_bp.route('/playoffs_panteras/')
def playoffs_panteras():
    eliminatorias = ['play-out', 'semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffPanteras.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/panteras_playoff.html', datos_playoff=datos_playoff)
    
# COPA CPLV MUNIA PANTERAS
# Crear formulario para la copa
@panteras_route_bp.route('/crear_copa_panteras', methods=['GET', 'POST'])
def crear_copa_panteras():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'cuartos': 3,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaPanteras(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                resultadoA = request.form.get(f'resultadoA{i}', ''),
                resultadoB = request.form.get(f'resultadoB{i}', ''),
                visitante = request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('panteras_route_bp.ver_copa_panteras'))
    return render_template('admin/copa/copa_panteras.html')
# Ver encuentros copa en Admin
@panteras_route_bp.route('/copa_panteras/')
def ver_copa_panteras():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaPanteras.query.filter_by(eliminatoria=eliminatoria).order_by(CopaPanteras.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_panteras.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@panteras_route_bp.route('/modificar_copa_panteras/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_panteras(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaPanteras.query.get(int(partido_id))
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
        flash('Copa actualizado correctamente', 'success')
        return redirect(url_for('panteras_route_bp.ver_copa_panteras'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_copa_aula'))
# Eliminar los partidos de la copa
@panteras_route_bp.route('/eliminar_copa_panteras/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_panteras(eliminatoria):
    partidos = CopaPanteras.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('panteras_route_bp.ver_copa_panteras'))
# Mostrar la copa del CPLV Munia Panteras
@panteras_route_bp.route('/copas_panteras/')
def copas_panteras():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaPanteras.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa[eliminatoria] = partidos   
    return render_template('copas/panteras_copa.html', datos_copa=datos_copa)

# EUROPA CPLV MUNIA PANTERAS
# Crear formulario para los grupos de Europa CPLV Munia Panteras
@panteras_route_bp.route('/crear_europa_panteras', methods=['GET', 'POST'])
def crear_europa_panteras():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))     
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonus_local = request.form.get(f'bonusA')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonus_visitante = request.form.get(f'bonusB')
            visitante = request.form.get(f'visitante{i}')  
            # Crear una nueva instancia de Europa Panteras con los datos recibidos           
            nuevo_partido = EuropaPanteras(
                encuentros=encuentros,
                fecha=fecha or '',
                hora=hora or '',
                local=local or '',
                bonusA = bonus_local or '',
                resultadoA=resultadoA or '',
                resultadoB=resultadoB or '',
                bonusB = bonus_visitante or '',
                visitante=visitante or ''
            )
            # Agregar la instancia a la sesión y hacer commit
            db.session.add(nuevo_partido)       
        # Confirmar los cambios en la base de datos
        db.session.commit()       
        # Redirigir a la página para ver la Europa Panteras
        return redirect(url_for('panteras_route_bp.ver_europa_panteras'))
    # Renderizar el formulario para crear Europa Panteras
    return render_template('admin/europa/europa_panteras.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion(grupo, local, bonus_local, resultado_local, resultado_visitante, bonus_visitante, visitante):
    # Convertir los resultados a enteros
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    bonus_local = int(bonus_local) if bonus_local and str(bonus_local).isdigit() else 0
    bonus_visitante = int(bonus_visitante) if bonus_visitante and str(bonus_visitante).isdigit() else 0

    # Consultar si los equipos ya están en la clasificación
    clasificacion_local = Clasificacion.query.filter_by(grupo=grupo, equipo=local).first()
    clasificacion_visitante = Clasificacion.query.filter_by(grupo=grupo, equipo=visitante).first()

    # Crear si no existen
    if not clasificacion_local:
        clasificacion_local = Clasificacion(grupo=grupo, equipo=local, jugados=0, ganados=0, empatados=0 , perdidos=0, puntos=0, bonus=0)
        db.session.add(clasificacion_local)

    if not clasificacion_visitante:
        clasificacion_visitante = Clasificacion(grupo=grupo, equipo=visitante, jugados=0, ganados=0, empatados=0 , perdidos=0, puntos=0, bonus=0)
        db.session.add(clasificacion_visitante)

    # Actualizar partidos jugados y puntos
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_local.jugados += 1
        clasificacion_visitante.jugados += 1

        if resultado_local > resultado_visitante:
            clasificacion_local.ganados += 1
            clasificacion_local.puntos += 3
            clasificacion_visitante.perdidos += 1
            clasificacion_visitante.puntos += 0
        elif resultado_local < resultado_visitante:
            clasificacion_visitante.ganados += 1
            clasificacion_visitante.puntos += 3
            clasificacion_local.perdidos += 1
            clasificacion_local.puntos += 0
        else:
            # Empate: ambos suman 1 + sus bonus
            clasificacion_local.puntos += 1 + bonus_local
            clasificacion_visitante.puntos += 1 + bonus_visitante

    # Guardar los cambios
    db.session.commit()
    return clasificacion_local, clasificacion_visitante
# Recalcular clasificación
def recalcular_clasificaciones(partidos):
    clasificaciones = {}
    enfrentamientos_directos = {}
    for partido in partidos:
        grupo = partido.encuentros
        local = partido.local
        visitante = partido.visitante
        bonus_local = int(partido.bonusA) if partido.bonusA.isdigit() else None
        resultado_local = int(partido.resultadoA) if partido.resultadoA.isdigit() else None
        resultado_visitante = int(partido.resultadoB) if partido.resultadoB.isdigit() else None
        bonus_visitante = int(partido.bonusB) if partido.bonusB.isdigit() else None
        if grupo not in clasificaciones:
            clasificaciones[grupo] = {}
        if local not in clasificaciones[grupo]:
            clasificaciones[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones[grupo]:
            clasificaciones[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones[grupo][local]['jugados'] += 1
            clasificaciones[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones[grupo][local]['ganados'] += 1
                clasificaciones[grupo][local]['puntos'] += 3
                clasificaciones[grupo][visitante]['perdidos'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 0
            elif resultado_local < resultado_visitante:
                clasificaciones[grupo][visitante]['ganados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 3
                clasificaciones[grupo][local]['perdidos'] += 1
                clasificaciones[grupo][local]['puntos'] += 0
            elif resultado_local == resultado_visitante:
                clasificaciones[grupo][visitante]['empatados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 1 + bonus_visitante
                clasificaciones[grupo][local]['empatados'] += 1 
                clasificaciones[grupo][local]['puntos'] += 1 + bonus_local    
            
            clasificaciones[grupo][local]['bonus'] += bonus_local
            clasificaciones[grupo][visitante]['bonus'] += bonus_visitante       
        if local not in enfrentamientos_directos:
            enfrentamientos_directos[local] = {}
        if visitante not in enfrentamientos_directos:
            enfrentamientos_directos[visitante] = {}
        if resultado_local is not None and resultado_visitante is not None:
            enfrentamientos_directos[local][visitante] = resultado_local - resultado_visitante
            enfrentamientos_directos[visitante][local] = resultado_visitante - resultado_local        
    return clasificaciones, enfrentamientos_directos
# Función para obtener equipos desde la base de datos
def obtener_equipos_desde_bd(partidos):
    # Obtener todos los partidos de la base de datos
    partidos = EuropaPanteras.query.order_by(EuropaPanteras.id).all()
    # Definir los grupos y fases de eliminatorias
    grupos = {'grupoA', 'grupoB'}
    fases_eliminatorias = {'semifinales', 'final'}
    equipos_por_encuentros = {}
    eliminatorias = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        # Asumimos que 'encuentros' es un campo que puede ser 'grupoA', 'semifinales', etc.
        grupo_o_fase = partido.encuentros
        if grupo_o_fase in fases_eliminatorias:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros:
                equipos_por_encuentros[grupo_o_fase] = {'equipos': [], 'partidos': []}          
            # Creamos los diccionarios de los equipos
            local = {'nombre': partido.local, 'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0, 'bonus': 0}
            visitante = {'nombre': partido.visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0 ,'perdidos': 0, 'puntos': 0, 'bonus': 0}
            # Añadir equipos si no existen en la lista de equipos del grupo
            if not any(e['nombre'] == local['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in equipos_por_encuentros[grupo_o_fase]['equipos']):
                equipos_por_encuentros[grupo_o_fase]['equipos'].append(visitante)
            equipos_por_encuentros[grupo_o_fase]['partidos'].append(partido)
        else:
            print(f"Grupo o fase no reconocido: {grupo_o_fase}")
    return equipos_por_encuentros, eliminatorias
# Obtener equipos Europa Panteras
def obtener_europa_panteras():
    partidos = EuropaPanteras.query.order_by(EuropaPanteras.id).all()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros(partidos):
    encuentros = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'semifinales': {'id': 3, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 4, 'encuentros': 'final', 'partidos': []}
    }
    for partido in partidos:
        # Si el objeto 'partido' es de SQLAlchemy, accedemos a sus atributos con punto
        grupo = partido.encuentros  # Asumiendo que 'encuentros' es un campo en el modelo SQLAlchemy
        if grupo in encuentros:
            # Si el grupo existe, agregamos el partido a su lista
            encuentros[grupo]['partidos'].append(partido)
        else:
            # Si no encontramos el grupo, lo indicamos
            print(f"Grupo no encontrado: {grupo}")
    return encuentros
# Crear formularios para los grupos y eliminatorias CPLV Munia Panteras
@panteras_route_bp.route('/europa_panteras/')
def ver_europa_panteras():
    try:
        partidos = obtener_europa_panteras()
        dats9 = formatear_partidos_por_encuentros(partidos)
        print(dats9)
        return render_template('admin/europa/europa_panteras.html', dats9=dats9)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Europa de CPLV Munia Panteras: {e}")
        return render_template('error.html')
# Modificar los partidos de los playoff
@panteras_route_bp.route('/modificar_europa_panteras/<string:encuentros>', methods=['POST'])
def modificar_europa_panteras(encuentros):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                if not partido_id:
                    continue
                partido = EuropaPanteras.query.get(int(partido_id))
                if partido:
                    partido.fecha = request.form.get(f'fecha{i}', partido.fecha)
                    partido.hora = request.form.get(f'hora{i}', partido.hora)
                    partido.local = request.form.get(f'local{i}', partido.local)
                    partido.bousA = request.form.get(f'bonusA{i}', partido.bonusA)
                    partido.resultadoA = request.form.get(f'resultadoA{i}', partido.resultadoA)
                    partido.resultadoB = request.form.get(f'resultadoB{i}', partido.resultadoB)
                    partido.bonusB = request.form.get(f'bonusB{i}', partido.bonusB)
                    partido.visitante = request.form.get(f'visitante{i}', partido.visitante)
                    partido.encuentros = encuentros
            db.session.commit()
            flash('Partidos modificados correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error al modificar partidos: {e}")
            flash('Hubo un error al modificar los partidos', 'error')
        return redirect(url_for('panteras_route_bp.ver_europa_panteras'))
# Eliminar partidos Europa Panteras
@panteras_route_bp.route('/eliminar_europa_panteras/<string:identificador>', methods=['POST'])
def eliminar_europa_panteras(identificador):
    try:
        if identificador.startswith('grupo') or identificador in ['semifinales', 'final']:
            partidos = EuropaPanteras.query.filter_by(encuentros=identificador).all()
            for partido in partidos:
                db.session.delete(partido)
            db.session.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    return redirect(url_for('panteras_route_bp.ver_europa_panteras'))
# Ruta para mostrar la Europa CPLV Munia Panteras
@panteras_route_bp.route('/panteras_europa/')
def panteras_europa():
    partidos = obtener_europa_panteras()
    equipos_por_encuentros, eliminatorias = obtener_equipos_desde_bd(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones(partidos)
    # Definir fases eliminatorias que no deben entrar en las clasificaciones por grupo
    fases_eliminatorias = {'semifinales', 'final'}
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        if grupo in fases_eliminatorias:
            continue  # Saltar fases eliminatorias
        # Ordenar equipos según criterios
        equipos_ordenados = sorted(
            equipos.items(),
            key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados'])
        )
        # Criterio de desempate por enfrentamientos directos
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                return enfrentamientos_directos[equipo1][equipo2]
            return 0
        equipos_ordenados = sorted(
            equipos_ordenados,
            key=lambda item: (
                -item[1]['puntos'],
                item[1]['ganados'],
                item[1]['empatados'],
                item[1]['perdidos'],
                item[1]['bonus'],
                -item[1]['jugados'],
                
                -criterio_enfrentamientos_directos(item[0], item[0])
            )
        )
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template(
        'europa/panteras_europa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias,
        clasificaciones=data_clasificaciones
    )     

# SUPERCOPA ESPAÑA CPLV MUNIA PANTERAS
# Crear formulario para la supercopa
@panteras_route_bp.route('/crear_supercopa_panteras', methods=['GET', 'POST'])
def crear_supercopa_panteras():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = SupercopaPanteras(
                eliminatoria = eliminatoria,
                fecha = request.form.get(f'fecha{i}', ''),
                hora = request.form.get(f'hora{i}', ''),
                local = request.form.get(f'local{i}', ''),
                bonusA = request.form.get(f'bonusA{i}', ''),
                resultadoA = request.form.get(f'resultadoA{i}', ''),
                resultadoB = request.form.get(f'resultadoB{i}', ''),
                bonusB = request.form.get(f'bonusB{i}', ''),
                visitante = request.form.get(f'visitante{i}', '')
            )
            db.session.add(partido)
        db.session.commit()
        return redirect(url_for('panteras_route_bp.ver_supercopa_panteras'))
    return render_template('admin/supercopa/supercopa_panteras.html')
# Ver encuentros supercopa en Admin
@panteras_route_bp.route('/supercopa_panteras/')
def ver_supercopa_panteras():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaPanteras.query.filter_by(eliminatoria=eliminatoria).order_by(SupercopaPanteras.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/supercopa/supercopa_panteras.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la supercopa
@panteras_route_bp.route('/modificar_supercopa_panteras/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_supercopa_panteras(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = SupercopaPanteras.query.get(int(partido_id))
            if not partido_obj:
                continue
            partido_obj.fecha = request.form.get(f'fecha{i}', '')
            partido_obj.hora = request.form.get(f'hora{i}', '')
            partido_obj.local = request.form.get(f'local{i}', '')
            partido_obj.bonusA = request.form.get(f'bonusA{i}', '')
            partido_obj.resultadoA = request.form.get(f'resultadoA{i}', '')
            partido_obj.resultadoB = request.form.get(f'resultadoB{i}', '')
            partido_obj.bonusB = request.form.get(f'bonusB{i}', '')
            partido_obj.visitante = request.form.get(f'visitante{i}', '')
            partido_obj.orden = i
        # Commit para guardar los cambios
        db.session.commit()
        flash('Supercopa actualizado correctamente', 'success')
        return redirect(url_for('panteras_route_bp.ver_supercopa_panteras'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('panteras_route_bp.ver_supercopa_panteras'))
# Eliminar los partidos de la supercopa Ibérica
@panteras_route_bp.route('/eliminar_supercopa_panteras/<string:eliminatoria>', methods=['POST'])
def eliminar_supercopa_panteras(eliminatoria):
    partidos = SupercopaPanteras.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('panteras_route_bp.ver_supercopa_panteras'))
# Mostrar la supercopa del CPLV Munia Panteras
@panteras_route_bp.route('/supercopas_panteras/')
def supercopas_panteras():
    eliminatorias = ['semifinales', 'final']
    datos_supercopa = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaPanteras.query.filter_by(eliminatoria=eliminatoria).all()
        datos_supercopa[eliminatoria] = partidos   
    return render_template('supercopas/panteras_supercopa.html', datos_supercopa=datos_supercopa)     