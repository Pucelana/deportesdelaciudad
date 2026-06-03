from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime
from collections import defaultdict
from itertools import groupby
from sqlalchemy.orm import sessionmaker
from app.extensions import db
from ..models.salvador_fem import JornadaSalvadorFem, SalvadorFemPartido, SalvadorFemClub, PlayoffSalvadorFem, CopaSalvadorFem, SupercopaIbericaSalvadorFem, EuropaSalvadorFem, Clasificacion

salvador_fem_route_bp = Blueprint('salvador_fem_route_bp', __name__)

# LIGA SALVADOR
# Crear el calendario Salvador Fem.
@salvador_fem_route_bp.route('/crear_calendario_salvador_fem', methods=['GET', 'POST'])
def ingresar_resultado_salvador_fem():
    if request.method == 'POST':
        nombre_jornada = request.form['nombre']
        num_partidos = int(request.form['num_partidos'])       
        # Crear la jornada y añadirla a la sesión
        jornada = JornadaSalvadorFem(nombre=nombre_jornada)
        db.session.add(jornada)
        db.session.flush()  # Esto nos da el ID antes del commit        
        # Recorrer los partidos y añadirlos a la base de datos
        for i in range(num_partidos):

            local = request.form.get(f'local{i}')
            visitante = request.form.get(f'visitante{i}')

            resultadoA = request.form.get(f'resultadoA{i}')
            resultadoB = request.form.get(f'resultadoB{i}')
            # 🔥 CLAVE: ignorar partidos vacíos
            if not local or not visitante:
                continue

            partido = SalvadorFemPartido(
                jornada_id=jornada.id,
                fecha=request.form.get(f'fecha{i}'),
                hora=request.form.get(f'hora{i}'),
                local=local,
                visitante=visitante,
                resultadoA=resultadoA or "",
                resultadoB=resultadoB or "",
                bonusA=request.form.get(f'bonusA{i}') or 0,
                bonusB=request.form.get(f'bonusB{i}') or 0,
                orden=i
            )

            db.session.add(partido)
            # Confirmar todos los cambios en la base de datos
        db.session.commit()
        print("JORNADA:", jornada.nombre)
        print("PARTIDOS GUARDADOS:", len(jornada.partidos))
        # Redirigir al calendario después de crear la jornada
        return redirect(url_for('salvador_fem_route_bp.calendarios_salvador_fem'))
    # Si es un GET, renderizamos el formulario de creación
    return render_template('admin/calendarios/calend_salvador_fem.html')
# Ver calendario Salvador en Admin
@salvador_fem_route_bp.route('/calendario_salvador_fem')
def calendarios_salvador_fem():
    jornadas = JornadaSalvadorFem.query.order_by(JornadaSalvadorFem.id.asc()).all()
    # Ordenar los partidos por el campo `orden` en cada jornada
    for jornada in jornadas:
        jornada.partidos = db.session.query(SalvadorFemPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(SalvadorFemPartido.orden.asc())\
            .all()
    return render_template('admin/calendarios/calend_salvador_fem.html', jornadas=jornadas)
# Modificar jornada
@salvador_fem_route_bp.route('/modificar_jornada_salvador_fem/<int:id>', methods=['GET', 'POST'])
def modificar_jornada_salvador_fem(id):
    jornada = db.session.query(JornadaSalvadorFem).filter(JornadaSalvadorFem.id == id).first()
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
                partido = db.session.query(SalvadorFemPartido).filter(SalvadorFemPartido.id == partido_id).first()
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
            return redirect(url_for('salvador_fem_route_bp.calendarios_salvador_fem'))
    return render_template('admin/calendarios/calend_salvador_fem.html', jornada=jornada)
# Eliminar jornada
@salvador_fem_route_bp.route('/eliminar_jornada_salvador_fem/<int:id>', methods=['GET','POST'])
def eliminar_jornada_salvador_fem(id):
    # Obtener la jornada
    jornada = db.session.query(JornadaSalvadorFem).filter(JornadaSalvadorFem.id == id).first()   
    if jornada:
        # Eliminar los partidos asociados a la jornada
        db.session.query(SalvadorFemPartido).filter(SalvadorFemPartido.jornada_id == id).delete()
        # Eliminar la jornada
        db.session.delete(jornada)       
        # Confirmar los cambios en la base de datos
        db.session.commit()
    # Redirigir al calendario después de eliminar la jornada
    return redirect(url_for('salvador_fem_route_bp.calendarios_salvador_fem'))
# Obtener datos Salvador
def obtener_datos_salvador_fem():
    # Obtener todas las jornadas Salvador Fem.
    jornadas = JornadaSalvadorFem.query.all()
    jornadas_con_partidos = []
    for jornada in jornadas:
        # Obtener los partidos de esta jornada
        partidos = db.session.query(SalvadorFemPartido)\
            .filter_by(jornada_id=jornada.id)\
            .order_by(SalvadorFemPartido.orden.asc())\
            .all()       
        jornada_con_partidos = {
            'nombre': jornada.nombre,
            'partidos': partidos
        }       
        jornadas_con_partidos.append(jornada_con_partidos)     
    return jornadas_con_partidos
total_partidos_temporada_salvador_fem = 10
total_partidos_temporada_grupos_salvador_fem = 5
# Función para separar fases de la temporada
def separar_fases(data):
    fase_regular = []
    fase_liguilla = []

    for jornada in data:
        nombre = jornada['nombre'].lower()

        if "grupo a" in nombre or "grupo b" in nombre or "liguilla" in nombre:
            fase_liguilla.append(jornada)
        else:
            fase_regular.append(jornada)

    return fase_regular, fase_liguilla
# Calendario Salvador Fem
@salvador_fem_route_bp.route('/equipos_rugby/calendario_salvador_fem')
def calendario_salvador_fem():
    datos = obtener_datos_salvador_fem()
    nuevos_datos_salvador_fem = [dato for dato in datos if dato]
    equipo_salvador_fem = 'El Salvador Fem.'
    tabla_partidos_salvador_fem = {}
    # Iteramos sobre cada jornada y partido
    for jornada in datos:
        for partido in jornada['partidos']:
            equipo_local = partido.local
            equipo_visitante = partido.visitante
            resultado_local = partido.resultadoA
            resultado_visitante = partido.resultadoB                 
            # Verificamos si el Caja está jugando
            if equipo_local == equipo_salvador_fem or equipo_visitante == equipo_salvador_fem:
                # Determinamos el equipo contrario y los resultados
                if equipo_local == equipo_salvador_fem:
                    equipo_contrario = equipo_visitante
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_vrac = 'C'
                else:
                    equipo_contrario = equipo_local
                    resultado_a = resultado_local
                    resultado_b = resultado_visitante
                    rol_salvador_fem = 'F'                
                # Verificamos si el equipo contrario no está en la tabla
                if equipo_contrario not in tabla_partidos_salvador_fem:
                    tabla_partidos_salvador_fem[equipo_contrario] = {'jornadas': {}}                                       
                # Verificamos si es el primer o segundo enfrentamiento
                if 'primer_enfrentamiento' not in tabla_partidos_salvador_fem[equipo_contrario]:
                    tabla_partidos_salvador_fem[equipo_contrario]['primer_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoB'] = resultado_b
                elif 'segundo_enfrentamiento' not in tabla_partidos_salvador_fem[equipo_contrario]:
                    tabla_partidos_salvador_fem[equipo_contrario]['segundo_enfrentamiento'] = jornada['nombre']
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoAA'] = resultado_a
                    tabla_partidos_salvador_fem[equipo_contrario]['resultadoBB'] = resultado_b                 
                # Agregamos la jornada y resultados
                if jornada['nombre'] not in tabla_partidos_salvador_fem[equipo_contrario]['jornadas']:
                    tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']] = {
                        'resultadoA': resultado_a,
                        'resultadoB': resultado_b,
                        'rol_salvador_fem': rol_salvador_fem
                    }               
                # Asignamos los resultados según el rol del Vrac
                if equipo_local == equipo_contrario or equipo_visitante == equipo_contrario:
                    if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA']:
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoA'] = resultado_a
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoB'] = resultado_b
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_vrac
                    else:
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_vrac
                else:
                    if not tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA']:
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_vrac
                    else:
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoAA'] = resultado_a
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['resultadoBB'] = resultado_b
                        tabla_partidos_salvador_fem[equipo_contrario]['jornadas'][jornada['nombre']]['rol_salvador_fem'] = rol_vrac
    return render_template('equipos_rugby/calendario_salvador_fem.html', tabla_partidos_salvador_fem=tabla_partidos_salvador_fem, nuevos_datos_salvador_fem=nuevos_datos_salvador_fem)
# Jornada 0 Vrac
@salvador_fem_route_bp.route('/jornada0_salvador_fem', methods=['GET', 'POST'])
def jornada0_salvador_fem():
    if request.method == 'POST':
        if 'equipo' in request.form:
            club = request.form['equipo']
            if club:
                nuevo_club = SalvadorFemClub(nombre=club)
                db.session.add(nuevo_club)
                db.session.commit()
            return redirect(url_for('salvador_fem_route_bp.jornada0_salvador_fem'))
    clubs = SalvadorFemClub.query.all()  # Obtener todos los clubes de PostgreSQL
    return render_template('admin/clubs/clubs_salvador_fem.html', clubs=clubs) 
# Eliminar clubs jornada 0
@salvador_fem_route_bp.route('/eliminar_club_salvador_fem/<int:club_id>', methods=['POST'])
def eliminar_club_salvador_fem(club_id):
    club = SalvadorFemClub.query.get(club_id)
    if club:
        db.session.delete(club)
        db.session.commit()
    return redirect(url_for('salvador_fem_route_bp.jornada0_salvador_fem'))
# Crear la clasificación CPLV Caja
def generar_clasificacion_analisis_rugby_salvador_fem(data):
    clasificacion = defaultdict(lambda: {
        'puntos': 0,
        'jugados': 0,
        'ganados': 0,
        'empatados': 0,
        'perdidos': 0,
        'favor': 0,
        'contra': 0,
        'diferencia_goles': 0,
        'bonus': 0
    })

    for jornada in data:
        for partido in jornada['partidos']:
            if (
                partido.resultadoA in (None, '')
                or partido.resultadoB in (None, '')
            ):
                continue

            try:
                a = int(partido.resultadoA)
                b = int(partido.resultadoB)
                ba = int(partido.bonusA or 0)
                bb = int(partido.bonusB or 0)
            except:
                continue

            local = partido.local
            visitante = partido.visitante

            # RESULTADO BASE
            if a > b:
                clasificacion[local]['puntos'] += 4
                clasificacion[local]['ganados'] += 1
                clasificacion[visitante]['perdidos'] += 1

            elif a < b:
                clasificacion[visitante]['puntos'] += 4
                clasificacion[visitante]['ganados'] += 1
                clasificacion[local]['perdidos'] += 1

            else:
                clasificacion[local]['puntos'] += 2
                clasificacion[visitante]['puntos'] += 2
                clasificacion[local]['empatados'] += 1
                clasificacion[visitante]['empatados'] += 1

            # 🔥 BONUS SOLO SI ES 1
            if ba == 1:
                clasificacion[local]['bonus'] += 1
                clasificacion[local]['puntos'] += 1   # si bonus suma a puntos

            if bb == 1:
                clasificacion[visitante]['bonus'] += 1
                clasificacion[visitante]['puntos'] += 1

            # stats
            clasificacion[local]['jugados'] += 1
            clasificacion[visitante]['jugados'] += 1

            clasificacion[local]['favor'] += a
            clasificacion[local]['contra'] += b
            clasificacion[visitante]['favor'] += b
            clasificacion[visitante]['contra'] += a

            clasificacion[local]['diferencia_goles'] += (a - b)
            clasificacion[visitante]['diferencia_goles'] += (b - a)

    return [
        {'equipo': k, 'datos': v}
        for k, v in clasificacion.items()
    ]  
# Deshacer desempates
def aplicar_h2h_en_empates(clasificacion, data):

    for i in range(len(clasificacion)-1):

        equipo1 = clasificacion[i]
        equipo2 = clasificacion[i+1]

        if equipo1['datos']['puntos'] == equipo2['datos']['puntos']:

            ganador = None

            for jornada in data:
                for partido in jornada['partidos']:

                    local = partido.local
                    visitante = partido.visitante

                    if (
                        (local == equipo1['equipo'] and visitante == equipo2['equipo']) or
                        (local == equipo2['equipo'] and visitante == equipo1['equipo'])
                    ):

                        try:
                            a = int(partido.resultadoA)
                            b = int(partido.resultadoB)
                        except:
                            continue

                        if local == equipo1['equipo']:
                            if a > b:
                                ganador = equipo1['equipo']
                            elif b > a:
                                ganador = equipo2['equipo']
                        else:
                            if a > b:
                                ganador = equipo2['equipo']
                            elif b > a:
                                ganador = equipo1['equipo']

            if ganador == equipo2['equipo']:
                clasificacion[i], clasificacion[i+1] = clasificacion[i+1], clasificacion[i]

    return clasificacion
# Ruta para mostrar la clasificación y análisis del Vrac
@salvador_fem_route_bp.route('/equipos_rugby/clasif_analisis_salvador_fem')
def clasif_analisis_salvador_fem():
    data = obtener_datos_salvador_fem()
    fase_regular, fase_liguilla = separar_fases(data)

    # 🔥 1. CLASIFICACIÓN BASE (GENERAL)
    base = generar_clasificacion_analisis_rugby_salvador_fem(fase_regular)
    clubs = SalvadorFemClub.query.all()

    for club in clubs:
        if not any(e['equipo'] == club.nombre for e in base):
            base.append({
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
            })
    base_dict = {e['equipo']: e['datos'] for e in base}

    # 🔥 2. FUNCIÓN ARRASTRE LIGUILLA
    def sumar_liguilla(grupo_data):
        liga = generar_clasificacion_analisis_rugby_salvador_fem(grupo_data)

        resultado = {}

        for e in liga:
            equipo = e['equipo']

            datos_base = base_dict.get(equipo, {
                'puntos': 0,
                'jugados': 0,
                'ganados': 0,
                'empatados': 0,
                'perdidos': 0,
                'favor': 0,
                'contra': 0,
                'diferencia_goles': 0,
                'bonus': 0
            })

            d = e['datos']

            resultado[equipo] = {
                'puntos': datos_base['puntos'] + d['puntos'],
                'jugados': datos_base['jugados'] + d['jugados'],
                'ganados': datos_base['ganados'] + d['ganados'],
                'empatados': datos_base['empatados'] + d['empatados'],
                'perdidos': datos_base['perdidos'] + d['perdidos'],
                'favor': datos_base['favor'] + d['favor'],
                'contra': datos_base['contra'] + d['contra'],
                'diferencia_goles': datos_base['diferencia_goles'] + d['diferencia_goles'],
                'bonus': datos_base['bonus'] + d['bonus']
            }

        return [{'equipo': k, 'datos': v} for k, v in resultado.items()]

    # 🔥 3. GRUPOS
    grupoA_data = [j for j in fase_liguilla if "grupo a" in j['nombre'].lower()]
    grupoB_data = [j for j in fase_liguilla if "grupo b" in j['nombre'].lower()]

    grupoA = sumar_liguilla(grupoA_data)
    grupoB = sumar_liguilla(grupoB_data)

    # 🔥 4. ORDEN GENERAL
    clasificacion_general = sorted(
        base,
        key=lambda x: (
            x['datos']['puntos'],
            x['datos']['diferencia_goles'],
            x['datos']['favor']
        ),
        reverse=True
    )

    # 🔥 5. ORDEN GRUPOS
    grupoA = sorted(grupoA, key=lambda x: (
        x['datos']['puntos'],
        x['datos']['diferencia_goles'],
        x['datos']['favor']
    ), reverse=True)

    grupoB = sorted(grupoB, key=lambda x: (
        x['datos']['puntos'],
        x['datos']['diferencia_goles'],
        x['datos']['favor']
    ), reverse=True)

    # 🔥 6. INDEXADO
    clasificacion_general_indexed = [
        {'index': i + 1, **e}
        for i, e in enumerate(clasificacion_general)
    ]

    grupoA_indexed = [
        {'index': i + 1, **e}
        for i, e in enumerate(grupoA)
    ]

    grupoB_indexed = [
        {'index': i + 7, **e}
        for i, e in enumerate(grupoB)
    ]

    return render_template(
        'equipos_rugby/clasif_analisis_salvador_fem.html',
        clasificacion_general_indexed=clasificacion_general_indexed,
        grupoA2=grupoA_indexed,
        grupoB2=grupoB_indexed
    )

# PLAYOFF SALVADOR
# Crear formulario para los playoff
@salvador_fem_route_bp.route('/crear_playoff_salvador_fem', methods=['GET', 'POST'])
def crear_playoff_salvador_fem():
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
            partido = PlayoffSalvadorFem(
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
        return redirect(url_for('salvador_fem_route_bp.ver_playoff_salvador_fem'))
    return render_template('admin/playoffs/playoff_salvador_fem.html')
# Ver encuentros playoff en Admin
@salvador_fem_route_bp.route('/playoff_salvador_fem/')
def ver_playoff_salvador_fem():
    eliminatorias = ['cuartos' ,'semifinales', 'final']
    datos_eliminatorias = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffSalvadorFem.query.filter_by(eliminatoria=eliminatoria).order_by(PlayoffSalvadorFem.orden).all()
        datos_eliminatorias[eliminatoria] = partidos
    return render_template('admin/playoffs/playoff_salvador_fem.html', datos_eliminatorias=datos_eliminatorias)
# Modificar los partidos de los playoff
@salvador_fem_route_bp.route('/modificar_playoff_salvador_fem/<string:eliminatoria>', methods=['GET', 'POST'])
def modificar_playoff_salvador_fem(eliminatoria):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        for i in range(num_partidos):
            partido_id = request.form.get(f'partido_id{i}')
            if not partido_id:
                continue
            partido_obj = PlayoffSalvadorFem.query.get(int(partido_id))
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
        return redirect(url_for('salvador_fem_route_bp.ver_playoff_salvador_fem'))
    # Si el método es GET, retorna el flujo habitual (en este caso no es necesario cambiarlo)
    return redirect(url_for('salvador_fem_route_bp.ver_playoff_salvador_fem'))
# Eliminar los partidos de los playoff
@salvador_fem_route_bp.route('/eliminar_playoff_salvador_fem/<string:eliminatoria>', methods=['POST'])
def eliminar_playoff_salvador_fem(eliminatoria):
    partidos = PlayoffSalvadorFem.query.filter_by(eliminatoria=eliminatoria).all()
    for partido in partidos:
        db.session.delete(partido)
    db.session.commit()
    flash(f'Eliminatoria {eliminatoria} eliminada correctamente', 'success')
    return redirect(url_for('salvador_fem_route_bp.ver_playoff_salvador_fem'))
# Mostrar los playoffs del CPLV Caja Rural
@salvador_fem_route_bp.route('/playoffs_salvador_fem/')
def playoffs_salvador_fem():
    eliminatorias = ['cuartos', 'semifinales', 'final']
    datos_playoff = {}
    for eliminatoria in eliminatorias:
        partidos = PlayoffSalvadorFem.query.filter_by(eliminatoria=eliminatoria).all()
        datos_playoff[eliminatoria] = partidos   
    return render_template('playoff/salvador_playoff.html', datos_playoff=datos_playoff)

# COPA EL SALVADOR
# Crear formulario para los grupos de la Copa DH VRAC
@salvador_fem_route_bp.route('/crear_copa_salvador_fem', methods=['GET', 'POST'])
def crear_copa_salvador_fem():
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
            nuevo_partido = CopaSalvadorFem(
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
        return redirect(url_for('salvador_fem_route_bp.ver_copa_salvador_fem'))
    # Renderizar el formulario para crear la copa UEMC
    return render_template('admin/copa/copa_salvador_fem.html')
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
    partidos = CopaSalvadorFem.query.order_by(CopaSalvadorFem.id).all()
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
def obtener_copa_salvador_fem():
    partidos = CopaSalvadorFem.query.order_by(CopaSalvadorFem.id).all()
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
@salvador_fem_route_bp.route('/copa_salvador_fem/')
def ver_copa_salvador_fem():
    try:
        partidos = obtener_copa_salvador_fem()
        dats5 = formatear_partidos_por_encuentros(partidos)
        print(dats5)
        return render_template('admin/copa/copa_salvador_fem.html', dats5=dats5)
    except Exception as e:
        print(f"Error al obtener o formatear los datos de la Copa Salvador: {e}")
        return render_template('error.html')
# Modificar los partidos de los playoff
@salvador_fem_route_bp.route('/modificar_copa_salvador_fem/<string:encuentros>', methods=['POST'])
def modificar_copa_salvador_fem(encuentros):
    if request.method == 'POST':
        num_partidos = int(request.form.get('num_partidos', 0))
        try:
            for i in range(num_partidos):
                partido_id = request.form.get(f'partido_id{i}')
                if not partido_id:
                    continue
                partido = CopaSalvadorFem.query.get(int(partido_id))
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
        return redirect(url_for('salvador_fem_route_bp.ver_copa_salvador_fem'))
# Eliminar partidos Copa DH VRAC
@salvador_fem_route_bp.route('/eliminar_copa_salvador_fem/<string:identificador>', methods=['POST'])
def eliminar_copa_salvador_fem(identificador):
    try:
        if identificador.startswith('grupo') or identificador in ['semifinales', 'final']:
            partidos = CopaSalvadorFem.query.filter_by(encuentros=identificador).all()
            for partido in partidos:
                db.session.delete(partido)
            db.session.commit()
            flash('Partidos eliminados correctamente', 'success')
        else:
            flash('Identificador de encuentros no válido', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar partidos: {str(e)}', 'error')
    return redirect(url_for('salvador_fem_route_bp.ver_copa_salvador_fem'))
# Ruta para mostrar la Copa El Salvador Fem
@salvador_fem_route_bp.route('/salvador_copa_fem/')
def salvador_copa_fem():
    partidos = obtener_copa_salvador_fem()
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
        'copas/salvador_copa_fem.html', equipos_por_encuentros=equipos_por_encuentros, eliminatorias=eliminatorias,
        clasificaciones=data_clasificaciones
    )