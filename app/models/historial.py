def obtener_evolucion_puntos(jornadas, nombre_equipo, funcion_clasificacion):

    labels = []
    puntos = []

    jornadas_acumuladas = []

    for jornada in jornadas:

        jornadas_acumuladas.append({
            "nombre": jornada.nombre,
            "partidos": jornada.partidos
        })

        clasificacion = funcion_clasificacion(jornadas_acumuladas)

        labels.append(jornada.nombre)

        equipo = next(
            (
                e for e in clasificacion
                if e["equipo"] == nombre_equipo
            ),
            None
        )

        if equipo:
            puntos.append(equipo["datos"]["puntos"])
        else:
            puntos.append(0)

    return labels, puntos