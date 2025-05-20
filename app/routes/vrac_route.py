from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.vrac import JornadaVrac, VracPartido, VracClub, PlayoffVrac, CopaVrac, SupercopaIbericaVrac, EuropaVrac, Clasificacion

vrac_route_bp = Blueprint('vrac_route_bp', __name__)

# LIGA VRAC
# Crear el calendario Vrac
@vrac_route_bp.route('/crear_calendario_vrac', methods=['GET', 'POST'])
def ingresar_resultado_vrac():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaVrac(nombre=nombre_jornada)
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
            partido = VracPartido(
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
        return redirect(url_for('vrac_route_bp.calendarios_vrac'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_vrac.html')
# Ver calendario Vrac en Admin
@vrac_route_bp.route('/calendario_vrac')
def calendarios_vrac():
    jornadas = JornadaVrac.query.order_by(JornadaVrac.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(VracPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VracPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_vrac.html', jornadas=jornadas)
# Modificar jornada
@vrac_route_bp.route('/modificar_jornada_vrac/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_vrac(id):
    jornada = db.session.query(JornadaVrac).filter(JornadaVrac.id == id).first()
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
                partido = db.session.query(VracPartido).filter(VracPartido.id == partido_id).first()
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
            return redirect(url_for('vrac_route_bp.calendarios_vrac'))
    return render_template('admin/calendarios/calend_vrac.html', jornada=jornada)
# Eliminar jornada
@vrac_route_bp.route('/eliminar_jornada_vrac/<int:id>', methods=['GET','POST'])
def eliminar_jornada_vrac(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaVrac).filter(JornadaVrac.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(VracPartido).filter(VracPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('vrac_route_bp.calendarios_vrac'))
# Obtener datos Vrac
def obtener_datos_vrac():
    # Obtener todas las jornadas Vrac
    jornadas = JornadaVrac.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(VracPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(VracPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
total_partidos_temporada_vrac = 11
total_partidos_temporada_grupos_vrac = 5
# Calendario Vrac
@vrac_route_bp.route('/equipos_rugby/calendario_vrac')
def calendario_vrac():
    datos = obtener_datos_vrac()
    nuevos_datos_vrac = [dato for dato in datos if dato]
    equipo_vrac = 'DH VRAC'
    tabla_partidos_vrac = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_vrac or equipo_visitante == equipo_vrac:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_vrac:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vrac = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vrac = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_vrac:
                    tabla_partidos_vrac[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_vrac[equipo_contrario]:
                    tabla_partidos_vrac[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vrac[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_vrac[equipo_contrario]:
                    tabla_partidos_vrac[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_vrac[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_vrac[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_vrac[equipo_contrario]['jornadas']:
                    tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_vrac': rol_vrac
                    }               
                # Asignamos los resultados según el rol del Vrac
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                    else:
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                else:
                    if not tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
                    else:
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_vrac[equipo_contrario]['jornadas'][jornada['nombre']]['rol_vrac'] = rol_vrac
    return render_template('equipos_rugby/calendario_vrac.html', tabla_partidos_vrac=tabla_partidos_vrac, nuevos_datos_vrac=nuevos_datos_vrac)
# Jornada 0 Vrac
@vrac_route_bp.route('/jornada0_vrac', methods=['GET', 'POST'])
def jornada0_vrac():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = VracClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('vrac_route_bp.jornada0_vrac'))
    clubs = VracClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_vrac.html', clubs=clubs) 
# Eliminar clubs jornada 0
@vrac_route_bp.route('/eliminar_club_vrac/<int:club_id>', methods=['POST'])
def eliminar_club_vrac(club_id):
    club = VracClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('vrac_route_bp.jornada0_vrac'))
# Crear la clasificación CPLV Caja
def generar_clasificacion_analisis_rugby_vrac(data,total_partidos):
    default_dict = defaultdict(lambda: {})
    clasificacion = defaultdict(lambda: {'puntos': 0,'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            try:
                bonus_local = int(partido.bonusA)
                resultado_local = int(partido.resultadoA)
                resultado_visitante = int(partido.resultadoB)
                bonus_visitante = int(partido.bonusB)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if clasificacion[equipo_local]['jugados'] > 0:
                promedio_favor_local = clasificacion[equipo_local]['favor'] / clasificacion[equipo_local]['jugados']
            else:
                promedio_favor_local = 0
            # Ajusta la lógica según tus reglas para asignar puntos y calcular estadísticas en baloncesto
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_local]['empatados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_visitante]['empatados'] += 1                    
            # Calcula los bonus
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
    # Ordena la clasificación por puntos y diferencia de canastas
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    return clasificacion_ordenada
# Crear la clasificación para el GrupoA2 y GrupoB2 del VRAC
def generar_clasificacion_grupoA2_grupoB2(data, total_partidos):
    clasificacion = defaultdict(lambda: {'puntos': 0, 'jugados': 0, 'ganados': 0, 'empatados': 0, 'perdidos': 0, 'favor': 0, 'contra': 0, 'diferencia_goles': 0, 'bonus': 0})
    for jornada in data[:total_partidos]:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            try:
                bonus_local = int(partido.bonusA)
                resultado_local = int(partido.resultadoA)
                resultado_visitante = int(partido.resultadoB)
                bonus_visitante = int(partido.bonusB)
            except ValueError:
                print(f"Error al convertir resultados a enteros en el partido {partido}")
                continue
            if resultado_local > resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 4 + bonus_local
                clasificacion[equipo_local]['ganados'] += 1
                clasificacion[equipo_visitante]['puntos'] += 0 + bonus_visitante
                clasificacion[equipo_visitante]['perdidos'] += 1
            elif resultado_local < resultado_visitante:
                clasificacion[equipo_local]['puntos'] += 0 + bonus_local
                clasificacion[equipo_local]['perdidos'] += 1
                clasificacion[equipo_visitante]['puntos'] += 4 + bonus_visitante
                clasificacion[equipo_visitante]['ganados'] += 1
            else:
                clasificacion[equipo_local]['puntos'] += 2 + bonus_local
                clasificacion[equipo_visitante]['puntos'] += 2 + bonus_visitante
                clasificacion[equipo_local]['empatados'] += 1
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
    # Ordena la clasificación por puntos y diferencia de goles
    clasificacion_ordenada = [{'equipo': equipo, 'datos': datos} for equipo, datos in sorted(clasificacion.items(), key=lambda x: (x[1]['puntos'], x[1]['diferencia_goles']), reverse=True)]
    # Divide la clasificación en Grupo A y Grupo B
    grupoA2 = clasificacion_ordenada[:6]
    grupoB2 = clasificacion_ordenada[6:12]
    return grupoA2, grupoB2
# Ruta para mostrar la clasificación y análisis del Vrac
@vrac_route_bp.route('/equipos_rugby/clasif_analisis_vrac')
def clasif_analisis_vrac():
    data = obtener_datos_vrac()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_vrac = generar_clasificacion_analisis_rugby_vrac(data,total_partidos_temporada_vrac)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_vrac = VracClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_vrac:
        if not any(equipo['equipo'] == club.nombre for equipo in clasificacion_analisis_vrac):
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
            clasificacion_analisis_vrac.append(equipo)
    clasificacion_analisis_vrac = sorted(clasificacion_analisis_vrac, key=lambda x: (x['datos']['puntos'], x['datos']['diferencia_goles']), reverse=True)
    clasificacion_analisis_vrac_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(clasificacion_analisis_vrac)]
    data13 = obtener_datos_vrac()  # Asumiendo que usas la misma función para obtener los datos de los grupos
    grupoA2, grupoB2 = generar_clasificacion_grupoA2_grupoB2(data13, total_partidos_temporada_grupos_vrac)
    grupoA2_indexed = [{'index': i + 1, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoA2)]
    grupoB2_indexed = [{'index': i + 7, 'equipo': equipo['equipo'], 'datos': equipo['datos']} for i, equipo in enumerate(grupoB2)]
    return render_template('equipos_rugby/clasif_analisis_vrac.html', clasificacion_analisis_vrac=clasificacion_analisis_vrac_indexed, grupoA2=grupoA2_indexed, grupoB2=grupoB2_indexed)

# PLAYOFF DH VRAC
# Crear formulario para los playoff
@vrac_route_bp.route('/crear_playoff_vrac', methods=['GET', 'POST'])
def crear_playoff_vrac():
    if request.method == 'POST':
        eliminatoria = request.form.get('eliminatoria')       
        max_partidos = {
            'cuartos': 4,
            'semifinales': 2,
            'final': 1
        }.get(eliminatoria, 0)
        num_partidos_str = request.form.get('num_partidos', '0').strip()
        num_partidos = int(num_partidos_str) if num_partidos_str else 0
        if num_partidos < 0 or num_partidos > max_partidos:
            return "Número de partidos no válido"
        for i in range(num_partidos):
            partido = PlayoffVrac(
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
        return redirect(url_for('vrac_route_bp.ver_playoff_vrac'))
    return render_template('admin/playoffs/playoff_vrac.html')
# Ver encuentros playoff en Admin
@vrac_route_bp.route('/playoff_vrac/')
def ver_playoff_vrac():
    eliminatorias = ['cuartos' ,'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffVrac.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffVrac.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_vrac.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@vrac_route_bp.route('/modificar_playoff_vrac/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_vrac(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffVrac.query.get(int(partido_id))
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
        return redirect(url_for('vrac_route_bp.ver_playoff_vrac'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('vrac_route_bp.ver_playoff_vrac'))
# Eliminar los partidos de los playoff
@vrac_route_bp.route('/eliminar_playoff_vrac/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_vrac(eliminatoria):
    partidos = PlayoffVrac.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('vrac_route_bp.ver_playoff_vrac'))
# Mostrar los playoffs del CPLV Caja Rural
@vrac_route_bp.route('/playoffs_vrac/')
def playoffs_vrac():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffVrac.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/vrac_playoff.html', datos_playoff=datos_playoff)

# COPA DH VRAC
# Crear formulario para los grupos de la Copa DH VRAC
@vrac_route_bp.route('/crear_copa_vrac', methods=['GET', 'POST'])
def crear_copa_vrac():
    if request.method == 'POST':
        encuentros = request.form.get('encuentros')
        print(f"Encuentros: {encuentros}")
        num_partidos = int(request.form.get('num_partidos', 0))     
        for i in range(num_partidos):
            fecha = request.form.get(f'fecha{i}')
            hora = request.form.get(f'hora{i}')
            local = request.form.get(f'local{i}')
            bonusA = request.form.get(f'bonusA{i}')
            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            bonusB = request.form.get(f'bonusB{i}')
            visitante = request.form.get(f'visitante{i}')  
            # Crear una nueva instancia de CopaUemc con los datos recibidos           
            nuevo_partido = CopaVrac(
                encuentros=encuentros,
                fecha=fecha or '',
                hora=hora or '',
                local=local or '',
                bonusA=bonusA or '',
                resultadoA=resultadoA or '',
                resultadoB=resultadoB or '',
                bonusB=bonusB or '',
                visitante=visitante or ''
            )
            # Agregar la instancia a la sesión y hacer commit
            db.session.add(nuevo_partido)       
        # Confirmar los cambios en la base de datos
        db.session.commit()       
        # Redirigir a la página para ver la Copa UEMC
        return redirect(url_for('vrac_route_bp.ver_copa_vrac'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/copa/copa_vrac.html')
# Actualizar clasificación de los grupos
def actualizar_clasificacion(grupo, local, bonus_local ,resultado_local, resultado_visitante, bonus_visitante ,visitante):
    # Convertir los resultados a enteros
    resultado_local = int(resultado_local) if resultado_local.isdigit() else None
    resultado_visitante = int(resultado_visitante) if resultado_visitante.isdigit() else None
    # Consultar si los equipos ya están en la clasificación
    clasificacion_local = Clasificacion.query.filter_by(grupo=grupo, equipo=local).first()
    clasificacion_visitante = Clasificacion.query.filter_by(grupo=grupo, equipo=visitante).first()
    # Si el local no existe, lo creamos
    if not clasificacion_local:
        clasificacion_local = Clasificacion(grupo=grupo, equipo=local, jugados=0, ganados=0, empatados=0 ,perdidos=0, puntos=0, bonus=0)
        db.session.add(clasificacion_local)  
    # Si el visitante no existe, lo creamos
    if not clasificacion_visitante:
        clasificacion_visitante = Clasificacion(grupo=grupo, equipo=visitante, jugados=0, ganados=0, empatados=0 ,perdidos=0, puntos=0, bonus=0)
        db.session.add(clasificacion_visitante)   
    # Actualizar los partidos jugados
    if resultado_local is not None and resultado_visitante is not None:
        clasificacion_local.jugados += 1
        clasificacion_visitante.jugados += 1       
        # Determinar el resultado del partido y actualizar clasificaciones
        if resultado_local > resultado_visitante:
            clasificacion_local.ganados += 1
            clasificacion_local.puntos += 4 + bonus_local
            clasificacion_visitante.perdidos += 1
            clasificacion_visitante.puntos += 0 + bonus_visitante
        elif resultado_local < resultado_visitante:
            clasificacion_visitante.ganados += 1
            clasificacion_visitante.puntos += 4 + bonus_visitante
            clasificacion_local.perdidos += 1
            clasificacion_local.puntos += 0 + bonus_local
        elif resultado_local == resultado_visitante:
            clasificacion_visitante.empatados += 1
            clasificacion_visitante.puntos += 2 + bonus_visitante
            clasificacion_local.empatados += 1
            clasificacion_local.puntos += 2 + bonus_local   
        clasificacion_local.bonus += bonus_local
        clasificacion_visitante.bonus += bonus_visitante  
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
        bonus_local = int(partido.bonusA) if partido.bonusA.isdigit() else None
        bonus_visitante = int(partido.bonusB) if partido.bonusB.isdigit() else None
        if grupo not in clasificaciones:
            clasificaciones[grupo] = {}
        if local not in clasificaciones[grupo]:
            clasificaciones[grupo][local] = {'jugados': 0, 'ganados': 0, 'empatados': 0 ,'perdidos': 0, 'puntos': 0, 'bonus': 0}
        if visitante not in clasificaciones[grupo]:
            clasificaciones[grupo][visitante] = {'jugados': 0, 'ganados': 0, 'empatados': 0 ,'perdidos': 0, 'puntos': 0, 'bonus':0}
        if resultado_local is not None and resultado_visitante is not None:
            clasificaciones[grupo][local]['jugados'] += 1
            clasificaciones[grupo][visitante]['jugados'] += 1
            if resultado_local > resultado_visitante:
                clasificaciones[grupo][local]['ganados'] += 1
                clasificaciones[grupo][local]['puntos'] += 4 + bonus_local
                clasificaciones[grupo][visitante]['perdidos'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 0 + bonus_visitante
            elif resultado_local < resultado_visitante:
                clasificaciones[grupo][visitante]['ganados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 4 + bonus_visitante
                clasificaciones[grupo][local]['perdidos'] += 1
                clasificaciones[grupo][local]['puntos'] += 0 + bonus_local
            elif resultado_local == resultado_visitante:
                clasificaciones[grupo][visitante]['empatados'] += 1
                clasificaciones[grupo][visitante]['puntos'] += 2 + bonus_visitante
                clasificaciones[grupo][local]['empatados'] += 1
                clasificaciones[grupo][local]['puntos'] += 2 + bonus_local     
            clasificaciones[grupo][local]['puntos'] += 1
            clasificaciones[grupo][visitante]['puntos'] += 1      
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
    partidos = CopaVrac.query.order_by(CopaVrac.id).all()
    # Definir los grupos y fases de eliminatorias
    grupos = {'grupoA', 'grupoB', 'grupoC', 'grupoD'}
    fases_eliminatorias = {'semifinales', 'final'}
    equipos_por_encuentros = {}
    eliminatorias = {'semifinales': {'partidos': []}, 'final': {'partidos': []}}
    for partido in partidos:
        # Asumimos que 'encuentros' es un campo que puede ser 'grupoA', 'cuartos', etc.
        grupo_o_fase = partido.encuentros
        if grupo_o_fase in fases_eliminatorias:
            # Añadir partidos a la fase de eliminación correspondiente
            eliminatorias[grupo_o_fase]['partidos'].append(partido)
        elif grupo_o_fase in grupos:
            # Añadir equipos y partidos a los grupos
            if grupo_o_fase not in equipos_por_encuentros:
                equipos_por_encuentros[grupo_o_fase] = {'equipos': [], 'partidos': []}          
            # Creamos los diccionarios de los equipos
            local = {'nombre': partido.local, 'jugados': 0, 'ganados': 0, 'empatados': 0 ,'perdidos': 0, 'puntos': 0, 'bonus': 0}
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
# Obtener equipos Copa UEMC
def obtener_copa_vrac():
    partidos = CopaVrac.query.order_by(CopaVrac.id).all()
    print("Partidos desde la BD:", partidos)  # Añadir esta línea para depuración
    return partidos
# Formatear partidos por grupo
def formatear_partidos_por_encuentros(partidos):
    encuentros = {
        'grupoA': {'id': 1, 'encuentros': 'grupoA', 'partidos': []},
        'grupoB': {'id': 2, 'encuentros': 'grupoB', 'partidos': []},
        'grupoC': {'id': 3, 'encuentros': 'grupoC', 'partidos': []},
        'grupoD': {'id': 4, 'encuentros': 'grupoD', 'partidos': []},
        'semifinales': {'id': 5, 'encuentros': 'semifinales', 'partidos': []},
        'final': {'id': 6, 'encuentros': 'final', 'partidos': []}
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
@vrac_route_bp.route('/copa_vrac/')
def ver_copa_vrac():
    try:
        partidos = obtener_copa_vrac()
        dats5 = formatear_partidos_por_encuentros(partidos)
        print(dats5)
        return render_template('admin/copa/copa_vrac.html', dats5=dats5)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de la Copa VRAC: {e}")
        return render_template('error.html')
# Modificar los partidos de los playoff
@vrac_route_bp.route('/modificar_copa_vrac/<string:encuentros>', methods=['POST'])
def modificar_copa_vrac(encuentros):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                if not partido_id:
                    continue
                partido = CopaVrac.query.get(int(partido_id))
                if partido:
                    partido.fecha = request.form.get(f'fecha{i}', partido.fecha)
                    partido.hora = request.form.get(f'hora{i}', partido.hora)
                    partido.local = request.form.get(f'local{i}', partido.local)
                    partido.bonusA = request.form.get(f'bonusA{i}', partido.bonusA)
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
        return redirect(url_for('vrac_route_bp.ver_copa_vrac'))
# Eliminar partidos Copa DH VRAC
@vrac_route_bp.route('/eliminar_copa_vrac/<string:identificador>', methods=['POST'])
def eliminar_copa_vrac(identificador):
    try:
        if identificador.startswith('grupo') or identificador in ['semifinales', 'final']:
            partidos = CopaVrac.query.filter_by(encuentros=identificador).all()
            for partido in partidos:
                db.session.delete(partido)
            db.session.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    return redirect(url_for('vrac_route_bp.ver_copa_vrac'))
# Ruta para mostrar la Copa DH VRAC
@vrac_route_bp.route('/vrac_copa/')
def vrac_copa():
    partidos = obtener_copa_vrac()
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
            key=lambda item: (-item[1]['puntos'], item[1]['ganados'], item[1]['perdidos'], item[1]['empatados'] , item[1]['jugados'], -item[1]['bonus'])
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
                item[1]['jugados'],
                -item[1]['bonus']
                -criterio_enfrentamientos_directos(item[0], item[0])
            )
        )
        data_clasificaciones[grupo] = equipos_ordenados
    return render_template(
        'copas/vrac_copa.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias,
        clasificaciones=data_clasificaciones
    )