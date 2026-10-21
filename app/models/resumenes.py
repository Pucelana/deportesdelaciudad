
from app.extensions import db
from datetime import datetime, timezone

class ResumenJornada(db.Model):
    __tablename__ = "resumenes_jornada"

    id = db.Column(db.Integer, primary_key=True)

    deporte = db.Column(db.String(30), nullable=False)
    equipo = db.Column(db.String(80), nullable=False)
    competicion = db.Column(db.String(100))
    temporada = db.Column(db.String(20))
    jornada = db.Column(db.String(30))

    # Fecha que aparecerá en el historial
    fecha = db.Column(db.Date, nullable=False, index=True)
    # Periodo al que pertenece el resumen semanal
    fecha_inicio = db.Column(db.Date, nullable=True, index=True)
    fecha_fin = db.Column(db.Date, nullable=True, index=True)

    rival = db.Column(db.String(100))
    resultado = db.Column(db.String(30))
    titular = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

    publicado = db.Column(db.Boolean, nullable=False, default=True)

    fecha_creacion = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
