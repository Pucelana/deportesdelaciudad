from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub, PlayoffRecoletas, CopaRecoletas,CopaEspañaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas, ClasificacionEuropa

recoletas_route_bp = Blueprint('recoletas_route_bp', __name__)

# LIGA RECOLETAS ATL.VALLADOLID
# Crear el calendario Recoletas Atl.Valladolid
@recoletas_route_bp.route('/crear_calendario_recoletas', methods=['GET', 'POST'])
def ingresar_resultado_recoletas():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaRecoletas(nombre=nombre_jornada)
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
            partido = RecoletasPartido(
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
        return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_recoletas.html')
# Ver calendario Atl.Valladolid en Admin
@recoletas_route_bp.route('/calendario_recoletas')
def calendarios_recoletas():
    jornadas = JornadaRecoletas.query.order_by(JornadaRecoletas.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(RecoletasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(RecoletasPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_recoletas.html', jornadas=jornadas)
# Modificar jornada
@recoletas_route_bp.route('/modificar_jornada_recoletas/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_recoletas(id):
    jornada = db.session.query(JornadaRecoletas).filter(JornadaRecoletas.id == id).first()
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
                partido = db.session.query(RecoletasPartido).filter(RecoletasPartido.id == partido_id).first()
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
            return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))
    return render_template('admin/calendarios/calend_recoletas.html', jornada=jornada)
# Eliminar jornada
@recoletas_route_bp.route('/eliminar_jornada_recoletas/<int:id>', methods=['GET','POST'])
def eliminar_jornada_recoletas(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaRecoletas).filter(JornadaRecoletas.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(RecoletasPartido).filter(RecoletasPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('recoletas_route_bp.calendarios_recoletas'))    
# Obtener datos Atl.Valladolid
def obtener_datos_recoletas():
    # Obtener todas las jornadas Atl.Valladolid
    jornadas = JornadaRecoletas.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(RecoletasPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(RecoletasPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Atl.Valladolid
@recoletas_route_bp.route('/equipos_balonmano/calendario_recoletas')
def calendario_recoletas():
    datos = obtener_datos_recoletas()
    nuevos_datos_recoletas = [dato for dato in datos if dato]
    equipo_recoletas = 'Atl.Valladolid'
    tabla_partidos_recoletas = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Aula está jugando
            if equipo_local == equipo_recoletas or equipo_visitante == equipo_recoletas:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_recoletas:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_recoletas = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_recoletas:
                    tabla_partidos_recoletas[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_recoletas[equipo_contrario]:
                    tabla_partidos_recoletas[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_recoletas[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_recoletas[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_recoletas[equipo_contrario]['jornadas']:
                    tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_recoletas': rol_recoletas
                    }               
                # Asignamos los resultados según el rol del Atl.Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                    else:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                else:
                    if not tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
                    else:
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_recoletas[equipo_contrario]['jornadas'][jornada['nombre']]['rol_recoletas'] = rol_recoletas
    return render_template('equipos_balonmano/calendario_recoletas.html', tabla_partidos_recoletas=tabla_partidos_recoletas, nuevos_datos_recoletas=nuevos_datos_recoletas)
# Jornada 0 Atl.Valladolid
@recoletas_route_bp.route('/jornada0_recoletas', methods=['GET', 'POST'])
def jornada0_recoletas():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = RecoletasClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('recoletas_route_bp.jornada0_recoletas'))
    clubs = RecoletasClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_recoletas.html', clubs=clubs)
# Eliminar clubs jornada 0
@recoletas_route_bp.route('/eliminar_club_recoletas/<int:club_id>', methods=['POST'])
def eliminar_club_recoletas(club_id):
    club = RecoletasClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('recoletas_route_bp.jornada0_recoletas'))
# Crear la clasificación Atl.Valladolid
def generar_clasificacion_analisis_balonmano_recoletas(data):
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
                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2
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
# Ruta para mostrar la clasificación y análisis del Atl.Valladolid
@recoletas_route_bp.route('/equipos_balonmano/clasif_analisis_recoletas')
def clasif_analisis_recoletas():
    data = obtener_datos_recoletas()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_recoletas = generar_clasificacion_analisis_balonmano_recoletas(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_recoletas = RecoletasClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_recoletas:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_recoletas):
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
            clasificacion_analisis_recoletas.append(equipo)
    return render_template('equipos_balonmano/clasif_analisis_recoletas.html',
        clasificacion_analisis_recoletas=clasificacion_analisis_recoletas)
    
# PLAYOFF ATL.VALLADOLID
# Crear formulario para los playoff
@recoletas_route_bp.route('/crear_playoff_recoletas', methods=['GET', 'POST'])
def crear_playoff_recoletas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'promocion': 2,
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffRecoletas(
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
        return redirect(url_for('recoletas_route_bp.ver_playoff_recoletas'))
    return render_template('admin/playoffs/playoff_recoletas.html')
# Ver encuentros playoff en Admin
@recoletas_route_bp.route('/playoff_recoletas/')
def ver_playoff_recoletas():
    eliminatorias = ['promocion']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffRecoletas.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffRecoletas.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_recoletas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@recoletas_route_bp.route('/modificar_playoff_recoletas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_recoletas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffRecoletas.query.get(int(partido_id))
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
        return redirect(url_for('recoletas_route_bp.ver_playoff_recoletas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('recoletas_route_bp.ver_playoff_recoletas'))
# Eliminar los partidos de los playoff
@recoletas_route_bp.route('/eliminar_playoff_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_recoletas(eliminatoria):
    partidos = PlayoffRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('recoletas_route_bp.ver_playoff_recoletas'))
# Mostrar los playoffs del Atl.Valladolid
@recoletas_route_bp.route('/playoffs_recoletas/')
def playoffs_recoletas():
    eliminatorias = ['promocion']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/recoletas_playoff.html', datos_playoff=datos_playoff)    
    
# COPA ATL.VALLADOLID
# Crear formulario para la copa
@recoletas_route_bp.route('/crear_copa_recoletas', methods=['GET', 'POST'])
def crear_copa_recoletas():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'ronda1': 12,
            'ronda2': 6,
            'octavos': 6,
            'cuartos': 4,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaRecoletas(
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
        return redirect(url_for('recoletas_route_bp.ver_copa_recoletas'))
    return render_template('admin/copa/copa_recoletas.html')
# Ver encuentros copa en Admin
@recoletas_route_bp.route('/copa_recoletas/')
def ver_copa_recoletas():
    eliminatorias = ['ronda1', 'ronda2', 'octavos', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaRecoletas.query.filter_by(eliminatoria=eliminatoria).order_by(CopaRecoletas.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_recoletas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@recoletas_route_bp.route('/modificar_copa_recoletas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_recoletas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaRecoletas.query.get(int(partido_id))
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
        return redirect(url_for('recoletas_route_bp.ver_copa_recoletas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('recoletas_route_bp.ver_copa_recoletas'))
# Eliminar los partidos de la copa
@recoletas_route_bp.route('/eliminar_copa_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_recoletas(eliminatoria):
    partidos = CopaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('recoletas_route_bp.ver_copa_recoletas'))
# Mostrar la copa del Atl.Valladolid
@recoletas_route_bp.route('/copas_recoletas/')
def copas_recoletas():
    eliminatorias = ['ronda1' ,'ronda2', 'octavos','cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa[eliminatoria] = partidos   
    return render_template('copas/recoletas_copa.html', datos_copa=datos_copa)

# COPA DE ESPAÑA ATL.VALLADOLID
# Crear formulario para la copa de españa
@recoletas_route_bp.route('/crear_copa_españa_recoletas', methods=['GET', 'POST'])
def crear_copa_españa_recoletas():
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
            partido = CopaEspañaRecoletas(
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
        return redirect(url_for('recoletas_route_bp.ver_copa_españa_recoletas'))
    return render_template('admin/copa/copa_recoletas.html')
# Ver encuentros copa en Admin
@recoletas_route_bp.route('/copa_recoletas/')
def ver_copa_españa_recoletas():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaEspañaRecoletas.query.filter_by(eliminatoria=eliminatoria).order_by(CopaEspañaRecoletas.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_recoletas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@recoletas_route_bp.route('/modificar_copa_españa_recoletas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_españa_recoletas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaRecoletas.query.get(int(partido_id))
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
        return redirect(url_for('recoletas_route_bp.ver_copa_españa_recoletas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('recoletas_route_bp.ver_copa_españa_recoletas'))
# Eliminar los partidos de la copa
@recoletas_route_bp.route('/eliminar_copa_españa_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_españa_recoletas(eliminatoria):
    partidos = CopaEspañaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('recoletas_route_bp.ver_copa_españa_recoletas'))
# Mostrar la copa del Atl.Valladolid
@recoletas_route_bp.route('/copas_españa_recoletas/')
def copas_españa_recoletas():
    eliminatorias = ['semifinales', 'final']
    datos_copa_españa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa_españa[eliminatoria] = partidos   
    return render_template('copas/recoletas_copa.html', datos_copa_españa=datos_copa_españa)

# # SUPERCOPA IBÉRICA ATL.VALLADOLID
# Crear formulario para la supercopa ibérica
@recoletas_route_bp.route('/crear_supercopa_iberica_recoletas', methods=['GET', 'POST'])
def crear_supercopa_iberica_recoletas():
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
            partido = SupercopaIbericaRecoletas(
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
        return redirect(url_for('recoletas_route_bp.ver_supercopa_iberica_recoletas'))
    return render_template('admin/supercopaIberica/supercopa_iberica_recoletas.html')
# Ver encuentros supercopa en Admin
@recoletas_route_bp.route('/supercopa_iberica_recoletas/')
def ver_supercopa_iberica_recoletas():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaIbericaRecoletas.query.filter_by(eliminatoria=eliminatoria).order_by(SupercopaIbericaRecoletas.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/supercopaIberica/supercopa_iberica_recoletas.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la supercopa ibérica
@recoletas_route_bp.route('/modificar_supercopa_iberica_recoletas/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_supercopa_iberica_recoletas(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = SupercopaIbericaRecoletas.query.get(int(partido_id))
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
        flash('Supercopa Ibérica actualizado correctamente', 'success')
        return redirect(url_for('recoletas_route_bp.ver_supercopa_iberica_recoletas'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('recoletas_route_bp.ver_supercopa_iberica_recoletas'))
# Eliminar los partidos de la supercopa Ibérica
@recoletas_route_bp.route('/eliminar_supercopa_iberica_recoletas/<string:eliminatoria>', methods=['POST'])
def eliminar_supercopa_iberica_recoletas(eliminatoria):
    partidos = SupercopaIbericaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('recoletas_route_bp.ver_supercopa_iberica_recoletas'))
# Mostrar la supercopa del Atl:valladolid
@recoletas_route_bp.route('/supercopas_ibericas_recoletas/')
def supercopas_iberica_recoletas():
    eliminatorias = ['semifinales', 'final']
    datos_supercopa_iberica = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaIbericaRecoletas.query.filter_by(eliminatoria=eliminatoria).all()
        datos_supercopa_iberica[eliminatoria] = partidos   
    return render_template('supercopasIberica/recoletas_supercopa_iberica.html', datos_supercopa_iberica=datos_supercopa_iberica)

# EUROPA ATL.VALLADOLID
# Crear formulario para europa
@recoletas_route_bp.route('/crear_europa_recoletas', methods=['GET', 'POST'])
def crear_europa_recoletas():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        num_partidos = int(request.form.get('num_partidos', 0))     
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')  
            # Crear una nueva instancia de CopaUemc con los datos recibidos           
            nuevo_partido = EuropaRecoletas(
                encuentros=encuentros,
                fecha=fecha or '',
                hora=hora or '',
                local=local or '',
                resultadoA=resultadoA or '',
                resultadoB=resultadoB or '',
                visitante=visitante or ''
            )
            # Agregar la instancia a la sesión y hacer commit
            db.session.add(nuevo_partido)       
        # Confirmar los cambios en la base de datos
        db.session.commit()       
        # Redirigir a la página para ver la Copa UEMC
        return redirect(url_for('recoletas_route_bp.ver_europa_recoletas'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/europa/europa_recoletas.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion(grupo, local, resultado_local, resultado_visitante, visitante):
    # Convertir los resultados a enteros
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Consultar si los equipos ya están en la clasificación
    clasificacion_local = ClasificacionEuropa.query.filter_by(grupo=grupo, equipo=local).first()
    clasificacion_visitante = ClasificacionEuropa.query.filter_by(grupo=grupo, equipo=visitante).first()
    # Si el local no existe, lo creamos
    if not clasificacion_local:
        clasificacion_local = ClasificacionEuropa(grupo=grupo, equipo=local, jugados=0, ganados=0, perdidos=0, puntos=0)
        db.session.add(clasificacion_local)  
    # Si el visitante no existe, lo creamos
    if not clasificacion_visitante:
        clasificacion_visitante = ClasificacionEuropa(grupo=grupo, equipo=visitante, jugados=0, ganados=0, perdidos=0, puntos=0)
        db.session.add(clasificacion_visitante)   
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_local.jugados += 1
        clasificacion_visitante.jugados += 1       
        # Determinar el resultado del partido y actualizar clasificaciones
        if resultado_local > resultado_visitante:
            clasificacion_local.ganados += 1
            clasificacion_local.puntos += 2
            clasificacion_visitante.perdidos += 1
            clasificacion_visitante.puntos += 1
        elif resultado_local < resultado_visitante:
            clasificacion_visitante.ganados += 1
            clasificacion_visitante.puntos += 2
            clasificacion_local.perdidos += 1
            clasificacion_local.puntos += 1
        else:
            clasificacion_local.puntos += 1
            clasificacion_visitante.puntos += 1  
    # Guardar los cambios en la base de datos
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
        resultado_local = int(partido.resultadoA) if partido.resultadoA.isdigit() else None
        resultado_visitante = int(partido.resultadoB) if partido.resultadoB.isdigit() else None
        if grupo not in clasificaciones:
            clasificaciones[grupo] = {}
        if local not in clasificaciones[grupo]:
            clasificaciones[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0}
        if visitante not in clasificaciones[grupo]:
            clasificaciones[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'puntos': 0}
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones[grupo][local]['jugados'] += 1
            clasificaciones[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones[grupo][local]['ganados'] += 1
                clasificaciones[grupo][local]['puntos'] += 2
                clasificaciones[grupo][visitante]['perdidos'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 0
            elif resultado_local < resultado_visitante:
                clasificaciones[grupo][visitante]['ganados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 2
                clasificaciones[grupo][local]['perdidos'] += 1
                clasificaciones[grupo][local]['puntos'] += 0
            else: 
                clasificaciones[grupo][visitante]['empatados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 1
                clasificaciones[grupo][local]['empatados'] += 1
                clasificaciones[grupo][local]['puntos'] += 1         
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
    partidos = EuropaRecoletas.query.order_by(EuropaRecoletas.id).all()
    # Definir los grupos y fases de eliminatorias
    fase_preliminar = 'preliminar'
    grupos_iniciales = {'grupoA', 'grupoB', 'grupoC', 'grupoD', 'grupoE', 'grupoF', 'grupoG', 'grupoH'}
    segunda_fase_grupos = {'grupo1', 'grupo2', 'grupo3', 'grupo4'}
    fases_eliminatorias = {'octavos' ,'cuartos', 'semifinales', 'final'}
    equipos_por_encuentros = {}
    eliminatorias = {fase: {'partidos': []} for fase in fases_eliminatorias}
    preliminar = {'equipos': [], 'partidos': []}
    segunda_fase = {}
    # Procesamos los partidos
    for partido in partidos:
        fase = partido.encuentros
        if fase == fase_preliminar:
            # Añadir a fase preliminar
            local = {'nombre': partido.local, 'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido.visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0}
            if not any(e['nombre'] == local['nombre'] for e in preliminar['equipos']):
                preliminar['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in preliminar['equipos']):
                preliminar['equipos'].append(visitante)
            preliminar['partidos'].append(partido)
        elif fase in grupos_iniciales or fase in segunda_fase_grupos:
            # Determinamos si es grupo inicial o de segunda fase
            grupo_dict = equipos_por_encuentros if fase in grupos_iniciales else segunda_fase
            if fase not in grupo_dict:
                grupo_dict[fase] = {'equipos': [], 'partidos': []}
            local = {'nombre': partido.local, 'jugados': 0, 'ganados': 0, 'empatados': 0 ,'perdidos': 0, 'puntos': 0}
            visitante = {'nombre': partido.visitante, 'jugados': 0, 'ganados': 0, 'empatados': 0 , 'perdidos': 0, 'puntos': 0}
            if not any(e['nombre'] == local['nombre'] for e in grupo_dict[fase]['equipos']):
                grupo_dict[fase]['equipos'].append(local)
            if not any(e['nombre'] == visitante['nombre'] for e in grupo_dict[fase]['equipos']):
                grupo_dict[fase]['equipos'].append(visitante)
            grupo_dict[fase]['partidos'].append(partido)
        elif fase in fases_eliminatorias:
            eliminatorias[fase]['partidos'].append(partido)
        else:
            print(f"Fase no reconocida: {fase}")
    return preliminar, equipos_por_encuentros, segunda_fase, eliminatorias
# Obtener equipos Europa Atl.Valladolid
def obtener_europa_recoletas():
    partidos = EuropaRecoletas.query.order_by(EuropaRecoletas.id).all()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros(partidos):
    encuentros = {
        'preliminar':{'id':1, 'encuentros': 'preliminar', 'partidos':[]},
        'grupoA': {'id': 2, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 3, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 4, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 5, 'encuentros': 'grupoD', 'partidos': []},
        'grupoE': {'id': 6, 'encuentros': 'grupoE', 'partidos': []},
        'grupoF': {'id': 7, 'encuentros': 'grupoF', 'partidos': []},
        'grupoG': {'id': 8, 'encuentros': 'grupoG', 'partidos': []},
        'grupoH': {'id': 9, 'encuentros': 'grupoH', 'partidos': []},
        'grupo1': {'id': 10, 'encuentros': 'grupo1', 'partidos': []},
        'grupo2': {'id': 11, 'encuentros': 'grupo2', 'partidos': []},
        'grupo3': {'id': 12, 'encuentros': 'grupo3', 'partidos': []},
        'grupo4': {'id': 13, 'encuentros': 'grupo4', 'partidos': []},
        'octavos': {'id': 14, 'encuentros': 'octavos', 'partidos': []},
        'cuartos': {'id': 15, 'encuentros': 'cuartos', 'partidos': []},
        'semifinales': {'id': 16, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 17, 'encuentros': 'final', 'partidos': []}
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
# Crear formularios para los grupos y eliminatorias Atl.Valladolid
@recoletas_route_bp.route('/europa_recoletas/')
def ver_europa_recoletas():
    try:
        partidos = obtener_europa_recoletas()
        dats5 = formatear_partidos_por_encuentros(partidos)
        print(dats5)
        return render_template('admin/europa/europa_recoletas.html', dats5=dats5)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Europa del Atl.Valladolid: {e}")
        return f"Ocurrió un error: {e}", 500
# Modificar los partidos de los playoff
@recoletas_route_bp.route('/modificar_europa_recoletas/<string:encuentros>', methods=['POST'])
def modificar_europa_recoletas(encuentros):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                if not partido_id:
                    continue
                partido = EuropaRecoletas.query.get(int(partido_id))
                if partido:
                    partido.fecha = request.form.get(f'fecha{i}', partido.fecha)
                    partido.hora = request.form.get(f'hora{i}', partido.hora)
                    partido.local = request.form.get(f'local{i}', partido.local)
                    partido.resultadoA = request.form.get(f'resultadoA{i}', partido.resultadoA)
                    partido.resultadoB = request.form.get(f'resultadoB{i}', partido.resultadoB)
                    partido.visitante = request.form.get(f'visitante{i}', partido.visitante)
                    partido.encuentros = encuentros
            db.session.commit()
            flash('Partidos modificados correctamente', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Error al modificar partidos: {e}")
            flash('Hubo un error al modificar los partidos', 'error')
        return redirect(url_for('recoletas_route_bp.ver_europa_recoletas'))
# Eliminar partidos Europa Atl.Valladolid
@recoletas_route_bp.route('/eliminar_europa_recoletas/<string:identificador>', methods=['POST'])
def eliminar_europa_recoletas(identificador):
    try:
        if identificador.startswith('grupo') or identificador in ['cuartos', 'semifinales', 'final']:
            partidos = EuropaRecoletas.query.filter_by(encuentros=identificador).all()
            for partido in partidos:
                db.session.delete(partido)
            db.session.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    return redirect(url_for('recoletas_route_bp.ver_europa_recoletas'))
# Ruta para mostrar la EuropaAtl.Valladolid
@recoletas_route_bp.route('/recoletas_europa/')
def recoletas_europa():
    partidos = obtener_europa_recoletas()
    preliminar, equipos_por_encuentros, segunda_fase, eliminatorias = obtener_equipos_desde_bd(partidos)
    clasificaciones, enfrentamientos_directos = recalcular_clasificaciones(partidos)
    data_clasificaciones = {}
    for grupo, equipos in clasificaciones.items():
        equipos_ordenados = sorted(equipos.items(), key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], -item[1]['jugados']))
        def criterio_enfrentamientos_directos(equipo1, equipo2):
            if equipo1 in enfrentamientos_directos and equipo2 in enfrentamientos_directos[equipo1]:
                resultado_directo = enfrentamientos_directos[equipo1][equipo2]
                return resultado_directo
            return 0
        equipos_ordenados = sorted(equipos_ordenados, key=lambda item: (
            -item[1]['puntos'],
            item[1]['ganados'],
            item[1]['perdidos'],
            -item[1]['jugados'],
            -criterio_enfrentamientos_directos(item[0], item[0])
        ))
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template('europa/recoletas_europa.html', equipos_por_encuentros=equipos_por_encuentros, segunda_fase=segunda_fase, eliminatorias=eliminatorias, preliminar=preliminar, clasificaciones=data_clasificaciones)