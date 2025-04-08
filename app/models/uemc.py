from app.extensions import db

class JornadaUEMC(db.Model):
    __tablename__ = 'jornadas_uemc'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('UEMCPartido', backref='jornada', cascade='all, delete-orphan')

class UEMCPartido(db.Model):
    __tablename__ = 'uemc_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_uemc.id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))   

class UEMCClub(db.Model):
    __tablename__ = 'uemc_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class CopaUEMC(db.Model):
    __tablename__ = 'copa_uemc'
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada partido
    encuentros = db.Column(db.String(255), nullable=True)  # Encuentros, por ejemplo, nombre del torneo o fase
    fecha = db.Column(db.Date, nullable=False)  # Fecha del partido
    hora = db.Column(db.Time, nullable=False)  # Hora del partido
    local = db.Column(db.String(255))  # Nombre del equipo local
    resultadoA = db.Column(db.String(120))  # Resultado del equipo local
    resultadoB = db.Column(db.String(120))  # Resultado del equipo visitante
    visitante = db.Column(db.String(255)) 