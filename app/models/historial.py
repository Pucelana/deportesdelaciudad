def obtener_evolucion_puntos(jornadas, nombre_equipo, funcion_clasificacion, campo="puntos"):

    labels = []
    valores = []

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
            valores.append(equipo["datos"].get(campo, 0))
        else:
            valores.append(0)

    return labels, valores