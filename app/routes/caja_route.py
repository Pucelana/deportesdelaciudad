from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.caja import JornadaCaja, CajaPartido, CajaClub, PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja

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