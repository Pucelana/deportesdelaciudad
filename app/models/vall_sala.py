from app.extensions import db

class TemporadaVallSala(db.Model):
    __tablename__ = "temporadas_vall_sala"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=False)
    jornadas = db.relationship(
        "JornadaVallSala",
        backref="temporada",
        cascade="all, delete-orphan"
    )
    
class JornadaVallSala(db.Model):
    __tablename__ = "jornadas_vall_sala"
    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(
        db.Integer,
        db.ForeignKey("temporadas_vall_sala.id", ondelete="CASCADE"),
        nullable=False
    )
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship(
        "VallSalaPartido",
        backref="jornada",
        cascade="all, delete-orphan"
    ) 
    
class VallSalaPartido(db.Model):
    __tablename__ = 'vall_sala_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_vall_sala.id'), nullable=False)
    fecha = db.Column(db.String(25))
    hora = db.Column(db.String(25))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)   

class VallSalaClub(db.Model):
    __tablename__ = 'vall_sala_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)
    
class CopaVallSala(db.Model):
    __tablename__ = 'copa_vall_sala'
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada partido
    eliminatoria = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(20))  # Fecha del partido
    hora = db.Column(db.String(20))  # Hora del partido
    local = db.Column(db.String(255))  # Nombre del equipo local
    resultadoA = db.Column(db.String(120))  # Resultado del equipo local
    resultadoB = db.Column(db.String(120))  # Resultado del equipo visitante
    visitante = db.Column(db.String(255))
    
class PlayoffVallSala(db.Model):
    __tablename__ = 'playoff_vall_sala'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer)    