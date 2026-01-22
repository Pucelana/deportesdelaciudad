from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from app.models.uemc import CopaUEMC
from ..models.aliados import JornadaAliados, AliadosPartido, AliadosClub, PlayoffAliados, CopaAliados, SupercopaAliados, EurocupAliados, Clasificacion

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
    return render_template('admin/calendarios/calend_aliados.html', jornadas=jornadas)
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

# PLAYOFF ALIADOS
# Crear formulario para los playoff
@aliados_route_bp.route('/crear_playoff_aliados', methods=['GET', 'POST'])
def crear_playoff_aliados():
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
            partido = PlayoffAliados(
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
        return redirect(url_for('aliados_route_bp.ver_playoff_aliados'))
    return render_template('admin/playoffs/playoff_aliados.html')
# Ver encuentros playoff en Admin
@aliados_route_bp.route('/playoff_aliados/')
def ver_playoff_aliados():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffAliados.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffAliados.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_aliados.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@aliados_route_bp.route('/modificar_playoff_aliados/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_aliados(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffAliados.query.get(int(partido_id))
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
        return redirect(url_for('aliados_route_bp.ver_playoff_aliados'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aliados_route_bp.ver_playoff_aliados'))
# Eliminar los partidos de los playoff
@aliados_route_bp.route('/eliminar_playoff_aliados/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_aliados(eliminatoria):
    partidos = PlayoffAliados.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aliados_route_bp.ver_playoff_aliados'))
# Mostrar los playoffs del Aliados
@aliados_route_bp.route('/playoffs_aliados/')
def playoffs_aliados():
    eliminatorias = ['semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffAliados.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/aliados_playoff.html', datos_playoff=datos_playoff)

# COPA ALIADOS
# Crear formulario para la copa
@aliados_route_bp.route('/crear_copa_aliados', methods=['GET', 'POST'])
def crear_copa_aliados():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'cuartos': 4,
            'semifinales': 2,
            'eliminados': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaAliados(
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
        return redirect(url_for('aliados_route_bp.ver_copa_aliados'))
    return render_template('admin/copa/copa_aliados.html')
# Ver encuentros copa en Admin
@aliados_route_bp.route('/copa_aliados/')
def ver_copa_aliados():
    eliminatorias = ['cuartos', 'semifinales', 'eliminados' , 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaAliados.query.filter_by(eliminatoria=eliminatoria).order_by(CopaAliados.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_aliados.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@aliados_route_bp.route('/modificar_copa_aliados/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_aliados(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaAliados.query.get(int(partido_id))
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
        return redirect(url_for('aliados_route_bp.ver_copa_aliados'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aliados_route_bp.ver_copa_aliados'))
# Eliminar los partidos de la copa
@aliados_route_bp.route('/eliminar_copa_aliados/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_aliados(eliminatoria):
    partidos = CopaAliados.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aliados_route_bp.ver_copa_aliados'))
# Mostrar la copa del Aliados
@aliados_route_bp.route('/copas_aliados/')
def copas_aliados():
    eliminatorias = ['cuartos', 'semifinales', 'eliminados' ,'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaAliados.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa[eliminatoria] = partidos   
    return render_template('copas/aliados_copa.html', datos_copa=datos_copa)

# SUPERCOPA ALIADOS
# Crear formulario para la supercopa
@aliados_route_bp.route('/crear_supercopa_aliados', methods=['GET', 'POST'])
def crear_supercopa_aliados():
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
            partido = SupercopaAliados(
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
        return redirect(url_for('aliados_route_bp.ver_supercopa_aliados'))
    return render_template('admin/supercopa/supercopa_aliados.html')
# Ver encuentros supercopa en Admin
@aliados_route_bp.route('/supercopa_aliados/')
def ver_supercopa_aliados():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaAliados.query.filter_by(eliminatoria=eliminatoria).order_by(SupercopaAliados.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/supercopa/supercopa_aliados.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la supercopa
@aliados_route_bp.route('/modificar_supercopa_aliados/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_supercopa_aliados(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = SupercopaAliados.query.get(int(partido_id))
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
        flash('Supercopa actualizado correctamente', 'success')
        return redirect(url_for('aliados_route_bp.ver_supercopa_aliados'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aliados_route_bp.ver_supercopa_aliados'))
# Eliminar los partidos de la copa
@aliados_route_bp.route('/eliminar_supercopa_aliados/<string:eliminatoria>', methods=['POST'])
def eliminar_supercopa_aliados(eliminatoria):
    partidos = SupercopaAliados.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aliados_route_bp.ver_supercopa_aliados'))
# Mostrar la supercopa del Aliados
@aliados_route_bp.route('/supercopas_aliados/')
def supercopas_aliados():
    eliminatorias = ['semifinales', 'final']
    datos_supercopa = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaAliados.query.filter_by(eliminatoria=eliminatoria).all()
        datos_supercopa[eliminatoria] = partidos   
    return render_template('supercopas/aliados_supercopa.html', datos_supercopa=datos_supercopa)      

# EUROCUP ALIADOS
@aliados_route_bp.route('/crear_eurocup_aliados', methods=['GET', 'POST'])
def crear_eurocup_aliados():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))     
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            visitante = request.form.get(f'visitante{i}')  
            # Crear una nueva instancia de EurocupAliados con los datos recibidos           
            nuevo_partido = EurocupAliados(
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
        return redirect(url_for('aliados_route_bp.ver_eurocup_aliados'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/europa/eurocup_aliados.html')
# Ver la Eurocup Aliados en Admin (crear/editar partidos)
@aliados_route_bp.route('/eurocup_aliados/')
def ver_eurocup_aliados():
    # Definimos todas las jornadas de la fase regular
    jornadas = ['liga_j1', 'liga_j2', 'liga_j3', 'liga_j4']
    # Y las fases de eliminatorias
    fases_eliminatorias = ['cuartos', 'semifinales', 'final']
    # Diccionario para la fase regular
    datos_jornadas = {j: EurocupAliados.query.filter_by(encuentros=j).order_by(EurocupAliados.id).all() for j in jornadas}
    # Diccionario para eliminatorias
    datos_eliminatorias = {f: EurocupAliados.query.filter_by(encuentros=f).order_by(EurocupAliados.id).all() for f in fases_eliminatorias}
    return render_template('admin/europa/eurocup_aliados.html',datos_jornadas=datos_jornadas, datos_eliminatorias=datos_eliminatorias)
# Actualizar clasificación de los grupos
def actualizar_clasificacion(local, resultado_local, resultado_visitante, visitante):
    # Convertir los resultados a enteros
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Consultar si los equipos ya están en la clasificación
    clasificacion_local = Clasificacion.query.filter_by(equipo=local).first()
    clasificacion_visitante = Clasificacion.query.filter_by( equipo=visitante).first()
    # Si el local no existe, lo creamos
    if not clasificacion_local:
        clasificacion_local = Clasificacion( equipo=local, jugados=0, ganados=0, perdidos=0, puntos=0, pf=0, pc=0)
        db.session.add(clasificacion_local)  
    # Si el visitante no existe, lo creamos
    if not clasificacion_visitante:
        clasificacion_visitante = Clasificacion( equipo=visitante, jugados=0, ganados=0, perdidos=0, puntos=0, pf=0, pc=0)
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
def obtener_jornadas_liga():
    jornadas = {}

    partidos = EurocupAliados.query.filter(
        EurocupAliados.encuentros.like('liga_%')
    ).order_by(EurocupAliados.orden, EurocupAliados.id).all()

    for partido in partidos:
        jornada = partido.encuentros  # liga_j1, liga_j2...
        if jornada not in jornadas:
            jornadas[jornada] = []
        jornadas[jornada].append(partido)
    return jornadas
def obtener_eliminatorias():
    fases = ['cuartos', 'semifinales', 'final']
    eliminatorias = {fase: [] for fase in fases}

    partidos = EurocupAliados.query.filter(EurocupAliados.encuentros.in_(fases)).order_by(EurocupAliados.orden).all()

    for partido in partidos:
        eliminatorias[partido.encuentros].append(partido)

    return eliminatorias
# Recalcular clasificación
def recalcular_clasificacion(jornadas):
    clasificacion = {}

    for jornada, partidos in jornadas.items():
        for p in partidos:
            if not p.local or not p.visitante:
                continue
            
            local = p.local.strip()
            visitante = p.visitante.strip()

            if local not in clasificacion:
                clasificacion[local] = {
                    'equipo': local, 'jugados': 0, 'ganados': 0,
                    'perdidos': 0, 'puntos': 0, 'favor': 0, 'contra': 0
                }

            if visitante not in clasificacion:
                clasificacion[visitante] = {
                    'equipo': visitante, 'jugados': 0, 'ganados': 0,
                    'perdidos': 0, 'puntos': 0, 'favor': 0, 'contra': 0
                }

            # 👉 si no hay resultado, NO se calcula nada más
            if not p.resultadoA or not p.resultadoB:
                continue

            if not p.resultadoA.isdigit() or not p.resultadoB.isdigit():
                continue

            resA = int(p.resultadoA)
            resB = int(p.resultadoB)

            clasificacion[local]['jugados'] += 1
            clasificacion[visitante]['jugados'] += 1

            clasificacion[local]['favor'] += resA
            clasificacion[local]['contra'] += resB
            clasificacion[visitante]['favor'] += resB
            clasificacion[visitante]['contra'] += resA

            if resA > resB:
                clasificacion[local]['ganados'] += 1
                clasificacion[local]['puntos'] += 2
                clasificacion[visitante]['perdidos'] += 1
                clasificacion[visitante]['puntos'] += 1
            elif resA < resB:
                clasificacion[visitante]['ganados'] += 1
                clasificacion[visitante]['puntos'] += 2
                clasificacion[local]['perdidos'] += 1
                clasificacion[local]['puntos'] += 1
            else:
                clasificacion[local]['puntos'] += 1
                clasificacion[visitante]['puntos'] += 1

    clasificacion_ordenada = sorted(
        clasificacion.items(),
        key=lambda x: (
            -x[1]["puntos"],
            -(x[1]["favor"] - x[1]["contra"]),
            -x[1]["favor"]
        )
    )

    return clasificacion_ordenada
# Modificar los partidos de los playoff
@aliados_route_bp.route('/modificar_eurocup_aliados/<string:encuentros>', methods=['POST'])
def modificar_eurocup_aliados(encuentros):
    try:
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            partido = EurocupAliados.query.get(int(partido_id))
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
    return redirect(url_for('aliados_route_bp.ver_eurocup_aliados'))
# Eliminar partidos Copa UEMC
@aliados_route_bp.route('/eliminar_eurocup_aliados/<string:identificador>', methods=['POST'])
def eliminar_eurocup_aliados(identificador):
    partidos = EurocupAliados.query.filter_by(encuentros=identificador).all()
    for p in partidos:
        db.session.delete(p)

    db.session.commit()
    return redirect(url_for('aliados_route_bp.ver_eurocup_aliados'))
# Mostrar la Copa UEMC
@aliados_route_bp.route('/aliados_eurocup/')
def aliados_eurocup():
    jornadas = obtener_jornadas_liga()
    clasificacion = recalcular_clasificacion(jornadas)
    eliminatorias = obtener_eliminatorias()
    return render_template('europa/aliados_eurocup.html', jornadas=jornadas, clasificacion=clasificacion, eliminatorias=eliminatorias
    )