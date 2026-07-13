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