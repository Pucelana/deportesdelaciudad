from datetime import datetime, date

def obtener_estadisticas_clasificacion(
    clasificacion,
    clubes,
    equipo,
    datos_por_defecto
):
    """
    Localiza al equipo en la clasificación, lo incorpora si todavía
    no aparece y devuelve sus datos y su posición.
    Los campos estadísticos dependen de cada deporte.
    """
    for club in clubes:
        if not any(
            fila["equipo"] == club.nombre
            for fila in clasificacion
        ):
            clasificacion.append({
                "equipo": club.nombre,
                "datos": datos_por_defecto.copy(),
            })

    datos_equipo = next(
        (
            fila["datos"]
            for fila in clasificacion
            if fila["equipo"] == equipo
        ),
        datos_por_defecto.copy()
    )

    posicion = next(
        (
            i + 1
            for i, fila in enumerate(clasificacion)
            if fila["equipo"] == equipo
        ),
        "--"
    )
    return posicion, datos_equipo

def obtener_ultimo_partido(equipos, competiciones):
    """
    Busca el partido más reciente entre las competiciones recibidas.

    equipos: nombre o lista de nombres con los que aparece el equipo.
    competiciones: lista de diccionarios con 'partidos' y 'nombre'.
    """

    if isinstance(equipos, str):
        equipos = [equipos]

    partidos_encontrados = []

    for competicion in competiciones:
        nombre_competicion = competicion["nombre"]

        for elemento in competicion["partidos"]:

            # Admite jornadas con partidos o partidos individuales.
            if isinstance(elemento, dict) and "partidos" in elemento:
                partidos = elemento["partidos"]
            else:
                partidos = [elemento]

            for partido in partidos:

                if not any(
                    nombre in (partido.local, partido.visitante)
                    for nombre in equipos
                ):
                    continue

                if (
                    partido.resultadoA in (None, "")
                    or partido.resultadoB in (None, "")
                ):
                    continue

                try:
                    fecha = datetime.strptime(
                        partido.fecha,
                        "%d.%m.%y"
                    )
                    goles_local = int(partido.resultadoA)
                    goles_visitante = int(partido.resultadoB)
                except (ValueError, TypeError):
                    continue

                partidos_encontrados.append({
                    "fecha": fecha,
                    "local": partido.local,
                    "visitante": partido.visitante,
                    "goles_local": goles_local,
                    "goles_visitante": goles_visitante,
                    "competicion": nombre_competicion,
                })

    return (
        max(partidos_encontrados, key=lambda p: p["fecha"])
        if partidos_encontrados else None
    )

def iterar_partidos_competiciones(competiciones):
    """
    Recorre los partidos de todas las competiciones.

    Las ligas contienen jornadas con una lista de partidos.
    Las copas y los playoffs contienen partidos directamente.
    """
    for competicion in competiciones:
        nombre_competicion = competicion["nombre"]
        tipo = competicion["tipo"]
        elementos = competicion["partidos"]

        for elemento in elementos:

            if tipo == "liga":
                partidos = elemento["partidos"]
                jornada = elemento["nombre"]
            else:
                partidos = [elemento]
                jornada = (
                    getattr(elemento, "encuentros", None)
                    or getattr(elemento, "eliminatoria", None)
                    or nombre_competicion
                )

            for partido in partidos:
                yield partido, nombre_competicion, jornada


def obtener_ultimo_partido(equipos, competiciones):
    """
    Devuelve el último partido disputado por el equipo,
    teniendo en cuenta todas las competiciones.
    """
    if isinstance(equipos, str):
        equipos = [equipos]

    partidos_encontrados = []

    for partido, nombre_competicion, jornada in iterar_partidos_competiciones(
        competiciones
    ):
        if not any(
            equipo in (partido.local, partido.visitante)
            for equipo in equipos
        ):
            continue

        if partido.resultadoA in (None, "") or partido.resultadoB in (None, ""):
            continue

        try:
            fecha_partido = datetime.strptime(
                partido.fecha, "%d.%m.%y"
            )
            goles_local = int(partido.resultadoA)
            goles_visitante = int(partido.resultadoB)
        except (ValueError, TypeError):
            continue

        partidos_encontrados.append({
            "fecha": fecha_partido,
            "local": partido.local,
            "visitante": partido.visitante,
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "competicion": nombre_competicion,
            "jornada": jornada,
        })

    return (
        max(partidos_encontrados, key=lambda p: p["fecha"])
        if partidos_encontrados else None
    )


def obtener_proximo_partido(equipos, competiciones):
    """
    Devuelve el próximo partido pendiente del equipo,
    teniendo en cuenta todas las competiciones.
    """
    if isinstance(equipos, str):
        equipos = [equipos]

    proximos_partidos = []
    hoy = date.today()

    for partido, nombre_competicion, jornada in iterar_partidos_competiciones(
        competiciones
    ):
        if not any(
            equipo in (partido.local, partido.visitante)
            for equipo in equipos
        ):
            continue

        if (
            partido.resultadoA not in (None, "")
            or partido.resultadoB not in (None, "")
        ):
            continue

        try:
            fecha_partido = datetime.strptime(
                partido.fecha, "%d.%m.%y"
            ).date()
        except (ValueError, TypeError):
            continue

        if fecha_partido < hoy:
            continue

        hora = partido.hora or ""

        try:
            hora_orden = datetime.strptime(
                hora, "%H:%M"
            ).time()
        except (ValueError, TypeError):
            hora_orden = datetime.max.time()

        proximos_partidos.append({
            "fecha": fecha_partido,
            "hora_orden": hora_orden,
            "hora": hora if hora else "--",
            "local": partido.local,
            "visitante": partido.visitante,
            "jornada": jornada,
            "competicion": nombre_competicion,
        })

    return (
        min(
            proximos_partidos,
            key=lambda p: (p["fecha"], p["hora_orden"])
        )
        if proximos_partidos else None
    )