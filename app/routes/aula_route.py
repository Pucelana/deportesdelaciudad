from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.aula import JornadaAula, AulaPartido, AulaClub, PlayoffAula, CopaAula, SupercopaIbericaAula, EuropaAula

aula_route_bp = Blueprint('aula_route_bp', __name__)

# LIGA AULA VALLADOLID
# Crear el calendario Aula Valladolid
@aula_route_bp.route('/crear_calendario_aula', methods=['GET', 'POST'])
def ingresar_resultado_aula():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaAula(nombre=nombre_jornada)
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
            partido = AulaPartido(
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
        return redirect(url_for('aula_route_bp.calendarios_aula'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_aula.html')
# Ver calendario Aula Valladolid en Admin
@aula_route_bp.route('/calendario_aula')
def calendarios_aula():
    jornadas = JornadaAula.query.order_by(JornadaAula.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(AulaPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(AulaPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_aula.html', jornadas=jornadas)
# Modificar jornada
@aula_route_bp.route('/modificar_jornada_aula/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_aula(id):
    jornada = db.session.query(JornadaAula).filter(JornadaAula.id == id).first()
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
                partido = db.session.query(AulaPartido).filter(AulaPartido.id == partido_id).first()
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
            return redirect(url_for('aula_route_bp.calendarios_aula'))
    return render_template('admin/calendarios/calend_aula.html', jornada=jornada)
# Eliminar jornada
@aula_route_bp.route('/eliminar_jornada_aula/<int:id>', methods=['GET','POST'])
def eliminar_jornada_aula(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaAula).filter(JornadaAula.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(AulaPartido).filter(AulaPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('aula_route_bp.calendarios_aula'))    
# Obtener datos Aula Valladolid
def obtener_datos_aula():
    # Obtener todas las jornadas RV aula
    jornadas = JornadaAula.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(AulaPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(AulaPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Aula Valladolid
@aula_route_bp.route('/equipos_balonmano/calendario_aula')
def calendario_aula():
    datos = obtener_datos_aula()
    nuevos_datos_aula = [dato for dato in datos if dato]
    equipo_aula = 'Aula Valladolid'
    tabla_partidos_aula = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Aula está jugando
            if equipo_local == equipo_aula or equipo_visitante == equipo_aula:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_aula:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aula = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_aula = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_aula:
                    tabla_partidos_aula[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_aula[equipo_contrario]:
                    tabla_partidos_aula[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aula[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_aula[equipo_contrario]:
                    tabla_partidos_aula[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_aula[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_aula[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_aula[equipo_contrario]['jornadas']:
                    tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_aula': rol_aula
                    }               
                # Asignamos los resultados según el rol del Aula Valladolid
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                    else:
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                else:
                    if not tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
                    else:
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_aula[equipo_contrario]['jornadas'][jornada['nombre']]['rol_aula'] = rol_aula
    return render_template('equipos_balonmano/calendario_aula.html', tabla_partidos_aula=tabla_partidos_aula, nuevos_datos_aula=nuevos_datos_aula)
# Jornada 0 Aula
@aula_route_bp.route('/jornada0_aula', methods=['GET', 'POST'])
def jornada0_aula():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = AulaClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('aula_route_bp.jornada0_aula'))
    clubs = AulaClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_aula.html', clubs=clubs)
# Eliminar clubs jornada 0
@aula_route_bp.route('/eliminar_club_aula/<int:club_id>', methods=['POST'])
def eliminar_club_aula(club_id):
    club = AulaClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('aula_route_bp.jornada0_aula'))
# Crear la clasificación Aula
def generar_clasificacion_analisis_balonmano_aula(data):
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
# Ruta para mostrar la clasificación y análisis del Aula
@aula_route_bp.route('/equipos_balonmano/clasif_analisis_aula')
def clasif_analisis_aula():
    data = obtener_datos_aula()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_aula = generar_clasificacion_analisis_balonmano_aula(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_aula = AulaClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_aula:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_aula):
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
            clasificacion_analisis_aula.append(equipo)
    return render_template('equipos_balonmano/clasif_analisis_aula.html',
        clasificacion_analisis_aula=clasificacion_analisis_aula)

# PLAYOFF AULA VALLADOLID
# Crear formulario para los playoff
@aula_route_bp.route('/crear_playoff_aula', methods=['GET', 'POST'])
def crear_playoff_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'cuartos': 8,
            'perdedores': 4,
            'septimo': 2,
            'cuarto': 2,
            'tercero': 2,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffAula(
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
        return redirect(url_for('aula_route_bp.ver_playoff_aula'))
    return render_template('admin/playoffs/playoff_aula.html')
# Ver encuentros playoff en Admin
@aula_route_bp.route('/playoff_aula/')
def ver_playoff_aula():
    eliminatorias = ['cuartos', 'perdedores', 'septimo', 'cuarto', 'tercero' ,'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffAula.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffAula.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@aula_route_bp.route('/modificar_playoff_aula/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_aula(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffAula.query.get(int(partido_id))
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
        return redirect(url_for('aula_route_bp.ver_playoff_aula'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_playoff_aula'))
# Eliminar los partidos de los playoff
@aula_route_bp.route('/eliminar_playoff_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_aula(eliminatoria):
    partidos = PlayoffAula.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aula_route_bp.ver_playoff_aula'))
# Mostrar los playoffs del Aula
@aula_route_bp.route('/playoffs_aula/')
def playoffs_aula():
    eliminatorias = ['cuartos', 'perdedores', 'septimo', 'cuarto', 'tercero', 'semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffAula.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/aula_playoff.html', datos_playoff=datos_playoff)

# COPA AULA VALLADOLID
# Crear formulario para la copa
@aula_route_bp.route('/crear_copa_aula', methods=['GET', 'POST'])
def crear_copa_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'fase1': 6,
            'fase2': 6,
            'cuartos': 4,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = CopaAula(
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
        return redirect(url_for('aula_route_bp.ver_copa_aula'))
    return render_template('admin/copa/copa_aula.html')
# Ver encuentros copa en Admin
@aula_route_bp.route('/copa_aula/')
def ver_copa_aula():
    eliminatorias = ['fase1', 'fase2', 'cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = CopaAula.query.filter_by(eliminatoria=eliminatoria).order_by(CopaAula.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/copa/copa_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la copa
@aula_route_bp.route('/modificar_copa_aula/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_copa_aula(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = CopaAula.query.get(int(partido_id))
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
        return redirect(url_for('aula_route_bp.ver_copa_aula'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_copa_aula'))
# Eliminar los partidos de la copa
@aula_route_bp.route('/eliminar_copa_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_copa_aula(eliminatoria):
    partidos = CopaAula.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aula_route_bp.ver_copa_aula'))
# Mostrar la copa del Aliados
@aula_route_bp.route('/copas_aula/')
def copas_aula():
    eliminatorias = ['fase1' ,'fase2', 'cuartos', 'semifinales', 'final']
    datos_copa = {}
    for eliminatoria in eliminatorias:
        partidos = CopaAula.query.filter_by(eliminatoria=eliminatoria).all()
        datos_copa[eliminatoria] = partidos   
    return render_template('copas/aula_copa.html', datos_copa=datos_copa)

# SUPERCOPA IBÉRICA AULA VALLADOLID
# Crear formulario para la supercopa
@aula_route_bp.route('/crear_supercopa_iberica_aula', methods=['GET', 'POST'])
def crear_supercopa_iberica_aula():
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
            partido = SupercopaIbericaAula(
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
        return redirect(url_for('aula_route_bp.ver_supercopa_iberica_aula'))
    return render_template('admin/supercopaIberica/supercopa_iberica_aula.html')
# Ver encuentros supercopa en Admin
@aula_route_bp.route('/supercopa_iberica_aula/')
def ver_supercopa_iberica_aula():
    eliminatorias = ['semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaIbericaAula.query.filter_by(eliminatoria=eliminatoria).order_by(SupercopaIbericaAula.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/supercopaIberica/supercopa_iberica_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la supercopa
@aula_route_bp.route('/modificar_supercopa_iberica_aula/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_supercopa_iberica_aula(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = SupercopaIbericaAula.query.get(int(partido_id))
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
        return redirect(url_for('aula_route_bp.ver_supercopa_iberica_aula'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_supercopa_iberica_aula'))
# Eliminar los partidos de la supercopa Ibérica
@aula_route_bp.route('/eliminar_supercopa_iberica_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_supercopa_iberica_aula(eliminatoria):
    partidos = SupercopaIbericaAula.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aula_route_bp.ver_supercopa_iberica_aula'))
# Mostrar la supercopa del Aula
@aula_route_bp.route('/supercopas_ibericas_aula/')
def supercopas_iberica_aula():
    eliminatorias = ['semifinales', 'final']
    datos_supercopa_iberica = {}
    for eliminatoria in eliminatorias:
        partidos = SupercopaIbericaAula.query.filter_by(eliminatoria=eliminatoria).all()
        datos_supercopa_iberica[eliminatoria] = partidos   
    return render_template('supercopasIberica/aula_supercopa_iberica.html', datos_supercopa_iberica=datos_supercopa_iberica)

# EUROPA AULA VALLADOLID
# Crear formulario para la copa
@aula_route_bp.route('/crear_europa_aula', methods=['GET', 'POST'])
def crear_europa_aula():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'ronda1': 64,
            'ronda2': 32,
            'octavos': 16,
            'cuartos': 8,
            'semifinales': 4,
            'final': 2
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = EuropaAula(
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
        return redirect(url_for('aula_route_bp.ver_europa_aula'))
    return render_template('admin/europa/europa_aula.html')
# Ver encuentros europa en Admin
@aula_route_bp.route('/europa_aula/')
def ver_europa_aula():
    eliminatorias = ['ronda1', 'ronda2', 'octavos','cuartos', 'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = EuropaAula.query.filter_by(eliminatoria=eliminatoria).order_by(EuropaAula.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/europa/europa_aula.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de la europa
@aula_route_bp.route('/modificar_europa_aula/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_europa_aula(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = EuropaAula.query.get(int(partido_id))
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
        flash('Europa actualizado correctamente', 'success')
        return redirect(url_for('aula_route_bp.ver_europa_aula'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('aula_route_bp.ver_europa_aula'))
# Eliminar los partidos de europa
@aula_route_bp.route('/eliminar_europa_aula/<string:eliminatoria>', methods=['POST'])
def eliminar_europa_aula(eliminatoria):
    partidos = EuropaAula.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('aula_route_bp.ver_europa_aula'))
# Mostrar europa de Aula Valladolid
@aula_route_bp.route('/europas_aula/')
def europas_aula():
    eliminatorias = ['ronda1' ,'ronda2', 'octavos','cuartos', 'semifinales', 'final']
    datos_europa = {}
    for eliminatoria in eliminatorias:
        partidos = EuropaAula.query.filter_by(eliminatoria=eliminatoria).all()
        datos_europa[eliminatoria] = partidos   
    return render_template('europa/aula_europa.html', datos_europa=datos_europa)     