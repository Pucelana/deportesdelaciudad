from app.routes.main import NOMBRES_EQUIPOS
def obtener_evolucion_puntos(jornadas, nombre_equipo, funcion_clasificacion, campo="puntos"):
    labels = []
    valores = []
    jornadas_acumuladas = []
    for jornada in jornadas:
        # Si jornada es un objeto SQLAlchemy
        if hasattr(jornada, "partidos"):
            jornadas_acumuladas.append({
                "nombre": jornada.nombre,
                "partidos": jornada.partidos
            })
            labels.append(jornada.nombre)
        # Si jornada ya es un diccionario
        else:
            jornadas_acumuladas.append(jornada)
            labels.append(jornada["nombre"])
        clasificacion = funcion_clasificacion(jornadas_acumuladas)
        nombres_validos = NOMBRES_EQUIPOS.get(
            nombre_equipo,
            [nombre_equipo]
        )

        equipo = next(
            (
                e for e in clasificacion
                if e["equipo"] in nombres_validos
            ),
            None
        )
        if equipo:
            valores.append(equipo["datos"].get(campo, 0))
        else:
            valores.append(0)
    return labels, valores

def obtener_evolucion_puntos_futbol(jornadas, nombre_equipo):
    labels = []
    valores = []
    puntos_acumulados = 0

    nombres_validos = NOMBRES_EQUIPOS.get(
        nombre_equipo,
        [nombre_equipo]
    )

    nombres_validos = set(nombres_validos)

    for jornada in jornadas:

        # Obtener nombre y partidos
        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        # Recorrer los partidos de la jornada
        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            # Puntos del Real Valladolid
            if local in nombres_validos:

                if r1 > r2:
                    puntos_acumulados += 3
                elif r1 == r2:
                    puntos_acumulados += 1

            elif visitante in nombres_validos:

                if r2 > r1:
                    puntos_acumulados += 3
                elif r1 == r2:
                    puntos_acumulados += 1

        labels.append(nombre_jornada)
        valores.append(puntos_acumulados)

    return labels, valores

def obtener_evolucion_puntos_hockey(jornadas, nombre_equipo):
    labels = []
    valores = []
    puntos_acumulados = 0

    nombres_validos = set(
        NOMBRES_EQUIPOS.get(nombre_equipo, [nombre_equipo])
    )

    for jornada in jornadas:

        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            # El equipo juega como local
            if local in nombres_validos:
                if r1 > r2:
                    puntos_acumulados += 3
                elif r1 == r2:
                    puntos_acumulados += 1

                try:
                    puntos_acumulados += int(partido.bonusA or 0)
                except (ValueError, TypeError):
                    pass

            # El equipo juega como visitante
            elif visitante in nombres_validos:
                if r2 > r1:
                    puntos_acumulados += 3
                elif r1 == r2:
                    puntos_acumulados += 1

                try:
                    puntos_acumulados += int(partido.bonusB or 0)
                except (ValueError, TypeError):
                    pass

        labels.append(nombre_jornada)
        valores.append(puntos_acumulados)

    return labels, valores

def obtener_evolucion_victorias_baloncesto(jornadas, nombre_equipo):
    labels = []
    valores = []
    victorias_acumuladas = 0

    nombres_validos = set(
        NOMBRES_EQUIPOS.get(nombre_equipo, [nombre_equipo])
    )

    for jornada in jornadas:

        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            if local in nombres_validos and r1 > r2:
                victorias_acumuladas += 1

            elif visitante in nombres_validos and r2 > r1:
                victorias_acumuladas += 1

        labels.append(nombre_jornada)
        valores.append(victorias_acumuladas)

    return labels, valores

def obtener_evolucion_puntos_balonmano(jornadas, nombre_equipo):
    labels = []
    valores = []
    puntos_acumulados = 0

    nombres_validos = NOMBRES_EQUIPOS.get(
        nombre_equipo,
        [nombre_equipo]
    )

    nombres_validos = set(nombres_validos)

    for jornada in jornadas:

        # Obtener nombre y partidos
        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        # Recorrer los partidos de la jornada
        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            # Puntos del Real Valladolid
            if local in nombres_validos:

                if r1 > r2:
                    puntos_acumulados += 2
                elif r1 == r2:
                    puntos_acumulados += 1

            elif visitante in nombres_validos:

                if r2 > r1:
                    puntos_acumulados += 2
                elif r1 == r2:
                    puntos_acumulados += 1

        labels.append(nombre_jornada)
        valores.append(puntos_acumulados)

    return labels, valores

def obtener_evolucion_puntos_rugby(jornadas, nombre_equipo):
    labels = []
    valores = []
    puntos_acumulados = 0

    nombres_validos = set(
        NOMBRES_EQUIPOS.get(nombre_equipo, [nombre_equipo])
    )

    for jornada in jornadas:

        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            # El equipo juega como local
            if local in nombres_validos:
                if r1 > r2:
                    puntos_acumulados += 4
                elif r1 == r2:
                    puntos_acumulados += 2

                try:
                    puntos_acumulados += int(partido.bonusA or 0)
                except (ValueError, TypeError):
                    pass

            # El equipo juega como visitante
            elif visitante in nombres_validos:
                if r2 > r1:
                    puntos_acumulados += 4
                elif r1 == r2:
                    puntos_acumulados += 2

                try:
                    puntos_acumulados += int(partido.bonusB or 0)
                except (ValueError, TypeError):
                    pass

        labels.append(nombre_jornada)
        valores.append(puntos_acumulados)

    return labels, valores

def obtener_evolucion_puntos_voley(jornadas, nombre_equipo):
    labels = []
    valores = []
    puntos_acumulados = 0

    nombres_validos = set(
        NOMBRES_EQUIPOS.get(nombre_equipo, [nombre_equipo])
    )

    for jornada in jornadas:

        if hasattr(jornada, "partidos"):
            nombre_jornada = jornada.nombre
            partidos = jornada.partidos
        else:
            nombre_jornada = jornada["nombre"]
            partidos = jornada["partidos"]

        for partido in partidos:

            local = partido.local
            visitante = partido.visitante

            r1 = partido.resultadoA
            r2 = partido.resultadoB

            if r1 in (None, "") or r2 in (None, ""):
                continue

            try:
                r1 = int(r1)
                r2 = int(r2)
            except (ValueError, TypeError):
                continue

            if local in nombres_validos:

                if r1 > r2:
                    puntos_acumulados += 3 if r1 == 3 and r2 <= 1 else 2
                else:
                    puntos_acumulados += 1 if r2 == 3 and r1 == 2 else 0

            elif visitante in nombres_validos:

                if r2 > r1:
                    puntos_acumulados += 3 if r2 == 3 and r1 <= 1 else 2
                else:
                    puntos_acumulados += 1 if r1 == 3 and r2 == 2 else 0

        labels.append(nombre_jornada)
        valores.append(puntos_acumulados)

    return labels, valores

from app.extensions import db

class Historial(db.Model):
    __tablename__ = "historial"
    id = db.Column(db.Integer, primary_key=True)
    deporte = db.Column(db.String(30), nullable=False)
    equipo = db.Column(db.String(80), nullable=False)
    temporada = db.Column(db.String(20), nullable=False)
    liga = db.Column(db.String(80))
    puntos = db.Column(db.Integer)
    puesto = db.Column(db.Integer)
    playoff = db.Column(db.String(80))
    copa = db.Column(db.String(80))
    europa = db.Column(db.String(80))
    titulos = db.Column(db.String(150))
    siguiente_temporada = db.Column(db.String(80))
    observaciones = db.Column(db.String(200))
    
class Palmaress(db.Model):
    __tablename__ = "palmaress"
    id = db.Column(db.Integer, primary_key=True)
    deporte = db.Column(db.String(30), nullable=False)
    equipo = db.Column(db.String(80), nullable=False)
    temporada = db.Column(db.String(20), nullable=False)
    competicion = db.Column(db.String(100))
    imagen = db.Column(db.String(100))
    orden = db.Column(db.Integer, default=0)    