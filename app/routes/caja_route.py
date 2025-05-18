from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.caja import JornadaCaja, CajaPartido, CajaClub, PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja, Clasificacion

caja_route_bp = Blueprint('caja_route_bp', __name__)

# LIGA CPLV CAJA
# Crear el calendario CPLV Caja
@caja_route_bp.route('/crear_calendario_caja', methods=['GET', 'POST'])
def ingresar_resultado_caja():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaCaja(nombre=nombre_jornada)
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
            partido = CajaPartido(
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
        return redirect(url_for('caja_route_bp.calendarios_caja'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_caja.html')
# Ver calendario CPLV Caja en Admin
@caja_route_bp.route('/calendario_caja')
def calendarios_caja():
    jornadas = JornadaCaja.query.order_by(JornadaCaja.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(CajaPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(CajaPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_caja.html', jornadas=jornadas)
# Modificar jornada
@caja_route_bp.route('/modificar_jornada_caja/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_caja(id):
    jornada = db.session.query(JornadaCaja).filter(JornadaCaja.id == id).first()
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
                partido = db.session.query(CajaPartido).filter(CajaPartido.id == partido_id).first()
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
            return redirect(url_for('caja_route_bp.calendarios_caja'))
    return render_template('admin/calendarios/calend_caja.html', jornada=jornada)
# Eliminar jornada
@caja_route_bp.route('/eliminar_jornada_caja/<int:id>', methods=['GET','POST'])
def eliminar_jornada_caja(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaCaja).filter(JornadaCaja.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(CajaPartido).filter(CajaPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('caja_route_bp.calendarios_caja'))    
# Obtener datos CPLV Caja
def obtener_datos_caja():
    # Obtener todas las jornadas CPLV Caja
    jornadas = JornadaCaja.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(CajaPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(CajaPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario CPLV Caja
@caja_route_bp.route('/equipos_hockey/calendario_caja')
def calendario_caja():
    datos = obtener_datos_caja()
    nuevos_datos_caja = [dato for dato in datos if dato]
    equipo_caja = 'CPLV Caja Rural'
    tabla_partidos_caja = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_caja or equipo_visitante == equipo_caja:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_caja:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_caja = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_caja = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_caja:
                    tabla_partidos_caja[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_caja[equipo_contrario]:
                    tabla_partidos_caja[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_caja[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_caja[equipo_contrario]:
                    tabla_partidos_caja[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_caja[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_caja[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_caja[equipo_contrario]['jornadas']:
                    tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_caja': rol_caja
                    }               
                # Asignamos los resultados según el rol del CPLV Caja
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                    else:
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                else:
                    if not tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
                    else:
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_caja[equipo_contrario]['jornadas'][jornada['nombre']]['rol_caja'] = rol_caja
    return render_template('equipos_hockey/calendario_caja.html', tabla_partidos_caja=tabla_partidos_caja, nuevos_datos_caja=nuevos_datos_caja)
# Jornada 0 CPLV Caja
@caja_route_bp.route('/jornada0_caja', methods=['GET', 'POST'])
def jornada0_caja():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = CajaClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('caja_route_bp.jornada0_caja'))
    clubs = CajaClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_caja.html', clubs=clubs)
# Eliminar clubs jornada 0
@caja_route_bp.route('/eliminar_club_caja/<int:club_id>', methods=['POST'])
def eliminar_club_caja(club_id):
    club = CajaClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('caja_route_bp.jornada0_caja'))
# Crear la clasificación CPLV Caja
def generar_clasificacion_analisis_hockey_caja(data):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0 })
    for jornada in data:
        for partido in jornada['partidos']:
            equipo_local = partido.local 
            equipo_visitante = partido.visitante
            bonus_local = partido.bonusA   
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB 
            bonus_visitante = partido.bonusB
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
# Ruta para mostrar la clasificación y análisis del CPLV Caja
@caja_route_bp.route('/equipos_hockey/clasif_analisis_caja')
def clasif_analisis_caja():
    data = obtener_datos_caja()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_caja = generar_clasificacion_analisis_hockey_caja(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_caja = CajaClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_caja:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_caja):
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
            clasificacion_analisis_caja.append(equipo)
    return render_template('equipos_hockey/clasif_analisis_caja.html',
        clasificacion_analisis_caja=clasificacion_analisis_caja)

# PLAYOFF CPLV CAJA RURAL
# Crear formulario para los playoff
@caja_route_bp.route('/crear_playoff_caja', methods=['GET', 'POST'])
def crear_playoff_caja():
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
            partido = PlayoffCaja(
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
        return redirect(url_for('caja_route_bp.ver_playoff_caja'))
    return render_template('admin/playoffs/playoff_caja.html')
# Ver encuentros playoff en Admin
@caja_route_bp.route('/playoff_caja/')
def ver_playoff_caja():
    eliminatorias = ['play-out' ,'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffCaja.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffCaja.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_caja.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@caja_route_bp.route('/modificar_playoff_caja/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_caja(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffCaja.query.get(int(partido_id))
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
        return redirect(url_for('caja_route_bp.ver_playoff_caja'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('caja_route_bp.ver_playoff_caja'))
# Eliminar los partidos de los playoff
@caja_route_bp.route('/eliminar_playoff_caja/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_caja(eliminatoria):
    partidos = PlayoffCaja.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('caja_route_bp.ver_playoff_caja'))
# Mostrar los playoffs del CPLV Caja Rural
@caja_route_bp.route('/playoffs_caja/')
def playoffs_caja():
    eliminatorias = ['play-out', 'semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffCaja.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/caja_playoff.html', datos_playoff=datos_playoff)

# COPA CPLV CAJA
# Crear formulario para la copa
@caja_route_bp.route('/crear_copa_caja', methods=['GET', 'POST'])
def crear_copa_caja():
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
            partido = CopaCaja(
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
        return redirect(url_for('caja_route_bp.ver_copa_caja'))
    return render_template('admin/copa/copa_caja.html')
# Ver encuentros copa en Admin
@caja_route_bp.route('/copa_caja/')
def ver_copa_caja():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaCaja.query.filter_by(eliminatoria=eliminatoria).order_by(CopaCaja.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_caja.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@caja_route_bp.route('/modificar_copa_caja/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_caja(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaCaja.query.get(int(partido_id))
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
        return redirect(url_for('caja_route_bp.ver_copa_caja'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_copa_aula'))
# Eliminar los partidos de la copa
@caja_route_bp.route('/eliminar_copa_caja/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_caja(eliminatoria):
    partidos = CopaCaja.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('caja_route_bp.ver_copa_caja'))
# Mostrar la copa del CPLV Caja
@caja_route_bp.route('/copas_caja/')
def copas_caja():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaCaja.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa[eliminatoria] = partidos   
    return render_template('copas/caja_copa.html', datos_copa=datos_copa)

# EUROPA CPLV CAJA RURAL
# Crear formulario para los grupos de Europa CPLV Caja Rural
@caja_route_bp.route('/crear_europa_caja', methods=['GET', 'POST'])
def crear_europa_caja():
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
            # Crear una nueva instancia de Europa Caja con los datos recibidos           
            nuevo_partido = EuropaCaja(
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
        # Redirigir a la página para ver la Europa Caja
        return redirect(url_for('caja_route_bp.ver_europa_caja'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/europa/europa_caja.html')
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
    partidos = EuropaCaja.query.order_by(EuropaCaja.id).all()
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
# Obtener equipos Europa Caja
def obtener_europa_caja():
    partidos = EuropaCaja.query.order_by(EuropaCaja.id).all()
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
# Crear formularios para los grupos y eliminatorias UEMC
@caja_route_bp.route('/europa_caja/')
def ver_europa_caja():
    try:
        partidos = obtener_europa_caja()
        dats8 = formatear_partidos_por_encuentros(partidos)
        print(dats8)
        return render_template('admin/europa/europa_caja.html', dats8=dats8)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de Europa de CPLV Caja Rural: {e}")
        return render_template('error.html')
# Modificar los partidos de los playoff
@caja_route_bp.route('/modificar_europa_caja/<string:encuentros>', methods=['POST'])
def modificar_europa_caja(encuentros):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                if not partido_id:
                    continue
                partido = EuropaCaja.query.get(int(partido_id))
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
        return redirect(url_for('caja_route_bp.ver_europa_caja'))
# Eliminar partidos Europa Caja
@caja_route_bp.route('/eliminar_europa_caja/<string:identificador>', methods=['POST'])
def eliminar_europa_caja(identificador):
    try:
        if identificador.startswith('grupo') or identificador in ['semifinales', 'final']:
            partidos = EuropaCaja.query.filter_by(encuentros=identificador).all()
            for partido in partidos:
                db.session.delete(partido)
            db.session.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    return redirect(url_for('caja_route_bp.ver_europa_caja'))
# Ruta para mostrar la Europa CPLV Caja
@caja_route_bp.route('/caja_europa/')
def caja_europa():
    partidos = obtener_europa_caja()
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
        'europa/caja_europa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias,
        clasificaciones=data_clasificaciones
    )    

# SUPERCOPA ESPAÑA CPLV CAJA RURAL
# Crear formulario para la supercopa
@caja_route_bp.route('/crear_supercopa_caja', methods=['GET', 'POST'])
def crear_supercopa_caja():
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
            partido = SupercopaCaja(
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
        return redirect(url_for('caja_route_bp.ver_supercopa_caja'))
    return render_template('admin/supercopa/supercopa_caja.html')
# Ver encuentros supercopa en Admin
@caja_route_bp.route('/supercopa_caja/')
def ver_supercopa_caja():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaCaja.query.filter_by(eliminatoria=eliminatoria).order_by(SupercopaCaja.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/supercopa/supercopa_caja.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la supercopa
@caja_route_bp.route('/modificar_supercopa_caja/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_supercopa_caja(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = SupercopaCaja.query.get(int(partido_id))
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
        return redirect(url_for('caja_route_bp.ver_supercopa_caja'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('caja_route_bp.ver_supercopa_caja'))
# Eliminar los partidos de la supercopa Ibérica
@caja_route_bp.route('/eliminar_supercopa_caja/<string:eliminatoria>', methods=['POST'])
def eliminar_supercopa_caja(eliminatoria):
    partidos = SupercopaCaja.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('caja_route_bp.ver_supercopa_caja'))
# Mostrar la supercopa del CPLV Caja
@caja_route_bp.route('/supercopas_caja/')
def supercopas_caja():
    eliminatorias = ['semifinales', 'final']
    datos_supercopa = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaCaja.query.filter_by(eliminatoria=eliminatoria).all()
        datos_supercopa[eliminatoria] = partidos   
    return render_template('supercopas/caja_supercopa.html', datos_supercopa=datos_supercopa)    