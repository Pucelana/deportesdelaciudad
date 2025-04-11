from app.extensions import db

class JornadaSimancas(db.Model):
    __tablename__ = 'jornadas_simancas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('SimancasPartido', backref='jornada', cascade='all, delete-orphan')
    
class SimancasPartido(db.Model):
    __tablename__ = 'simancas_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_simancas.id'), nullable=False)
    fecha = db.Column(db.String(25))
    hora = db.Column(db.Time, nullable=False)
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)   

class SimancasClub(db.Model):
    __tablename__ = 'simancas_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class CopaSimancas(db.Model):
    __tablename__ = 'copa_simancas'
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada partido
    eliminatoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(20))  # Fecha del partido
    hora = db.Column(db.String(20))  # Hora del partido
    local = db.Column(db.String(255))  # Nombre del equipo local
    resultadoA = db.Column(db.String(120))  # Resultado del equipo local
    resultadoB = db.Column(db.String(120))  # Resultado del equipo visitante
    visitante = db.Column(db.String(255))
    
class PlayoffSimancas(db.Model):
    __tablename__ = 'playoff_simancas'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer) 