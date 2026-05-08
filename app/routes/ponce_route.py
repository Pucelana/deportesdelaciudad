from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from functools import cmp_to_key
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.ponce import JornadaPonce, PoncePartido, PonceClub, PlayoffPonce, Clasificacion

ponce_route_bp = Blueprint('ponce_route_bp', __name__)

# LIGA PONCE
#Todo el proceso de calendario y clasificación del PONCE
# Ingresar los resultados de los partidos PONCE
@ponce_route_bp.route('/crear_calendario_ponce', methods=['GET', 'POST'])
def ingresar_resultado_ponce():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaPonce(nombre=nombre_jornada)
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
            partido = PoncePartido(
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
        return redirect(url_for('ponce_route_bp.calendarios_ponce'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_ponce.html')
# Ver calendario Ponce en Admin
@ponce_route_bp.route('/calendario_ponce')
def calendarios_ponce():
    jornadas = JornadaPonce.query.order_by(JornadaPonce.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(PoncePartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(PoncePartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_ponce.html', jornadas=jornadas)
# Modificar jornada
@ponce_route_bp.route('/modificar_jornada_ponce/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_ponce(id):
    jornada = db.session.query(JornadaPonce).filter(JornadaPonce.id == id).first()
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
                partido = db.session.query(PoncePartido).filter(PoncePartido.id == partido_id).first()
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
            return redirect(url_for('ponce_route_bp.calendarios_ponce'))        
    return render_template('admin/calendarios/calend_ponce.html', jornada=jornada)
# Eliminar jornada
@ponce_route_bp.route('/eliminar_jornada_ponce/<int:id>', methods=['GET','POST'])
def eliminar_jornada_ponce(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaPonce).filter(JornadaPonce.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(PoncePartido).filter(PoncePartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('ponce_route_bp.calendarios_ponce'))
# Obtener datos Ponce
def obtener_datos_ponce():
    # Obtener todas las jornadas Ponce
    jornadas = JornadaPonce.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = PoncePartido.query.filter_by(jornada_id=jornada.id).all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
# Calendario Ponce
@ponce_route_bp.route('/equipos_basket/calendario_ponce')
def calendario_ponce():
    datos = obtener_datos_ponce()
    nuevos_datos_ponce = [dato for dato in datos if dato]
    equipo_ponce = 'Ponce Valladolid CB'
    tabla_partidos_ponce = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Ponce está jugando
            if equipo_local == equipo_ponce or equipo_visitante == equipo_ponce:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_ponce:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_ponce = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_ponce = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_ponce:
                    tabla_partidos_ponce[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_ponce[equipo_contrario]:
                    tabla_partidos_ponce[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_ponce[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_ponce[equipo_contrario]:
                    tabla_partidos_ponce[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_ponce[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_ponce[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_ponce[equipo_contrario]['jornadas']:
                    tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_ponce': rol_ponce
                    }               
                # Asignamos los resultados según el rol del Ponce
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                    else:
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                else:
                    if not tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
                    else:
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_ponce[equipo_contrario]['jornadas'][jornada['nombre']]['rol_ponce'] = rol_ponce
    return render_template('equipos_basket/calendario_ponce.html', tabla_partidos_ponce=tabla_partidos_ponce, nuevos_datos_ponce=nuevos_datos_ponce)
# Jornada 0 Ponce
@ponce_route_bp.route('/jornada0_ponce', methods=['GET', 'POST'])
def jornada0_ponce():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = PonceClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('ponce_route_bp.jornada0_ponce'))
    clubs = PonceClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_ponce.html', clubs=clubs)
# Eliminar clubs jornada 0
@ponce_route_bp.route('/eliminar_club_ponce/<int:club_id>', methods=['POST'])
def eliminar_club_ponce(club_id):
    club = PonceClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('ponce_route_bp.jornada0_ponce'))
# Crear la clasificación Ponce
def generar_clasificacion_analisis_baloncesto_ponce(data):
    clasificacion = defaultdict(lambda: {
        'jugados': 0,
        'ganados': 0,
        'perdidos': 0,
        'favor': 0,
        'contra': 0,
        'diferencia_canastas': 0,
        'puntos': 0
    })

# GUARDAR ENFRENTAMIENTOS

    enfrentamientos = []

    for jornada in data:

        for partido in jornada['partidos']:

            equipo_local = partido.local
            equipo_visitante = partido.visitante

            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB

            # Saltar vacíos
            if (
                resultado_local is None
                or resultado_visitante is None
                or resultado_local == ''
                or resultado_visitante == ''
            ):
                continue

            try:

                resultado_local = int(resultado_local)
                resultado_visitante = int(resultado_visitante)

            except ValueError:
                continue

# CLASIFICACIÓN GENERAL

            if resultado_local > resultado_visitante:

                clasificacion[equipo_local]['puntos'] += 2
                clasificacion[equipo_local]['ganados'] += 1

                clasificacion[equipo_visitante]['puntos'] += 1
                clasificacion[equipo_visitante]['perdidos'] += 1

            else:

                clasificacion[equipo_visitante]['puntos'] += 2
                clasificacion[equipo_visitante]['ganados'] += 1

                clasificacion[equipo_local]['puntos'] += 1
                clasificacion[equipo_local]['perdidos'] += 1

            clasificacion[equipo_local]['jugados'] += 1
            clasificacion[equipo_visitante]['jugados'] += 1

            clasificacion[equipo_local]['favor'] += resultado_local
            clasificacion[equipo_local]['contra'] += resultado_visitante

            clasificacion[equipo_visitante]['favor'] += resultado_visitante
            clasificacion[equipo_visitante]['contra'] += resultado_local

            clasificacion[equipo_local]['diferencia_canastas'] += (
                resultado_local - resultado_visitante
            )

            clasificacion[equipo_visitante]['diferencia_canastas'] += (
                resultado_visitante - resultado_local
            )

# GUARDAR PARTIDO

            enfrentamientos.append({
                'local': equipo_local,
                'visitante': equipo_visitante,
                'puntos_local': resultado_local,
                'puntos_visitante': resultado_visitante
            })

    # =========================================================
    # MINI LIGA ENTRE EMPATADOS
    # =========================================================

    def clasificacion_particular(equipos_empatados):

        mini = defaultdict(lambda: {
            'victorias': 0,
            'derrotas': 0,
            'favor': 0,
            'contra': 0,
            'average': 0,
            'puntos': 0
        })

        for partido in enfrentamientos:

            local = partido['local']
            visitante = partido['visitante']

            if (
                local not in equipos_empatados
                or visitante not in equipos_empatados
            ):
                continue

            pl = partido['puntos_local']
            pv = partido['puntos_visitante']

            # FAVOR / CONTRA

            mini[local]['favor'] += pl
            mini[local]['contra'] += pv

            mini[visitante]['favor'] += pv
            mini[visitante]['contra'] += pl

            mini[local]['average'] += (pl - pv)
            mini[visitante]['average'] += (pv - pl)

            # VICTORIAS

            if pl > pv:

                mini[local]['victorias'] += 1
                mini[visitante]['derrotas'] += 1

                mini[local]['puntos'] += 2
                mini[visitante]['puntos'] += 1

            else:

                mini[visitante]['victorias'] += 1
                mini[local]['derrotas'] += 1

                mini[visitante]['puntos'] += 2
                mini[local]['puntos'] += 1

        return mini

    # =========================================================
    # COMPARADOR OFICIAL
    # =========================================================

    def comparar_equipos(a, b):

        nombre_a, datos_a = a
        nombre_b, datos_b = b

        # =========================================================
        # 1. PUNTOS GENERALES
        # =========================================================

        if datos_a['puntos'] != datos_b['puntos']:

            return datos_b['puntos'] - datos_a['puntos']

        # =========================================================
        # 2. EQUIPOS EMPATADOS
        # =========================================================

        equipos_empatados = []

        for equipo, datos in clasificacion.items():

            if datos['puntos'] == datos_a['puntos']:

                equipos_empatados.append(equipo)

        # =========================================================
        # 3. MINI LIGA
        # =========================================================

        if len(equipos_empatados) >= 2:

            mini = clasificacion_particular(equipos_empatados)

            mini_a = mini[nombre_a]
            mini_b = mini[nombre_b]

            # Puntos mini liga

            if mini_a['puntos'] != mini_b['puntos']:

                return mini_b['puntos'] - mini_a['puntos']

            # Average mini liga

            if mini_a['average'] != mini_b['average']:

                return mini_b['average'] - mini_a['average']

            # Favor mini liga

            if mini_a['favor'] != mini_b['favor']:

                return mini_b['favor'] - mini_a['favor']

        # =========================================================
        # 4. DIFERENCIA GENERAL
        # =========================================================

        if (
            datos_a['diferencia_canastas']
            != datos_b['diferencia_canastas']
        ):

            return (
                datos_b['diferencia_canastas']
                - datos_a['diferencia_canastas']
            )

        # =========================================================
        # 5. PUNTOS A FAVOR
        # =========================================================

        if datos_a['favor'] != datos_b['favor']:

            return datos_b['favor'] - datos_a['favor']

        return 0

    # =========================================================
    # ORDENAR
    # =========================================================

    equipos = list(clasificacion.items())

    equipos.sort(
        key=cmp_to_key(comparar_equipos)
    )

    # =========================================================
    # DEVOLVER
    # =========================================================

    return [
        {
            'equipo': equipo,
            'datos': datos
        }
        for equipo, datos in equipos
    ]
    
# Ruta para mostrar la clasificación y análisis del UEMC
@ponce_route_bp.route('/equipos_basket/clasif_analisis_ponce')
def clasif_analisis_ponce():
    data = obtener_datos_ponce()
    # Genera la clasificación y análisis actual
    clasificacion_analisis_ponce = generar_clasificacion_analisis_baloncesto_ponce(data)    
    # Obtén los equipos desde la base de datos PostgreSQL
    clubs_ponce = PonceClub.query.all()
    # Inicializa las estadísticas de los equipos que aún no están en la clasificación
    for club in clubs_ponce:
        if not any(
            equipo['equipo'] == club.nombre
            for equipo in clasificacion_analisis_ponce
        ):

            clasificacion_analisis_ponce.append({
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
            })

    clasificacion_analisis_ponce.sort(
        key=lambda x: x['datos']['puntos'],
        reverse=True
    )
    return render_template('equipos_basket/clasif_analisis_ponce.html',
        clasificacion_analisis_ponce=clasificacion_analisis_ponce)
    
# PLAYOFF PONCE
# Crear formulario para los playoff
@ponce_route_bp.route('/crear_playoff_ponce', methods=['GET', 'POST'])
def crear_playoff_ponce():
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
            nuevo_partido = PlayoffPonce(
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
        return redirect(url_for('ponce_route_bp.ver_playoff_ponce'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/playoffs/playoff_ponce.html')
# Ver encuentros playoff en Admin
@ponce_route_bp.route('/playoff_ponce/')
def ver_playoff_ponce():
    # Definimos todas las jornadas de la fase regular
    jornadas = ['liga_j1', 'liga_j2', 'liga_j3']
    # Y las fases de eliminatorias
    fases_eliminatorias = ['final_segundos']
    # Diccionario para la fase regular
    datos_jornadas = {j: PlayoffPonce.query.filter_by(encuentros=j).order_by(PlayoffPonce.id).all() for j in jornadas}
    # Diccionario para eliminatorias
    datos_eliminatorias = {f: PlayoffPonce.query.filter_by(encuentros=f).order_by(PlayoffPonce.id).all() for f in fases_eliminatorias}
    return render_template('admin/playoffs/playoff_ponce.html',datos_jornadas=datos_jornadas, datos_eliminatorias=datos_eliminatorias)
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

    partidos = PlayoffPonce.query.filter(
        PlayoffPonce.encuentros.like('liga_%')
    ).order_by(PlayoffPonce.orden, PlayoffPonce.id).all()

    for partido in partidos:
        jornada = partido.encuentros  # liga_j1, liga_j2...
        if jornada not in jornadas:
            jornadas[jornada] = []
        jornadas[jornada].append(partido)
    return jornadas
def obtener_eliminatorias():
    fases = ['final_segundos']
    eliminatorias = {fase: [] for fase in fases}

    partidos = PlayoffPonce.query.filter(PlayoffPonce.encuentros.in_(fases)).order_by(PlayoffPonce.orden).all()

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
@ponce_route_bp.route('/modificar_playoff_ponce/<string:encuentros>', methods=['POST'])
def modificar_playoff_ponce(encuentros):
    try:
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            partido = PlayoffPonce.query.get(int(partido_id))
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
    return redirect(url_for('ponce_route_bp.ver_playoff_ponce'))
# Eliminar los partidos de los playoff
@ponce_route_bp.route('/eliminar_playoff_ponce/<string:identificador>', methods=['POST'])
def eliminar_playoff_ponce(identificador):
    partidos = PlayoffPonce.query.filter_by(encuentros=identificador).all()
    for p in partidos:
        db.session.delete(p)

    db.session.commit()
    return redirect(url_for('ponce_route_bp.ver_playoff_ponce'))
# Mostrar los playoffs del Ponce
@ponce_route_bp.route('/playoffs_ponce/')
def playoff_ponce():
    jornadas = obtener_jornadas_liga()
    clasificacion = recalcular_clasificacion(jornadas)
    eliminatorias = obtener_eliminatorias()
    return render_template('playoff/ponce_playoff.html', jornadas=jornadas, clasificacion=clasificacion, eliminatorias=eliminatorias
    )    