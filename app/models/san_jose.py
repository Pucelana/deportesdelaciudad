from app.extensions import db

class TemporadaJose(db.Model):
    __tablename__ = "temporadas_san_jose"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=False)
    jornadas = db.relationship(
        "JornadaJose",
        backref="temporada",
        cascade="all, delete-orphan"
    )
    
class JornadaJose(db.Model):
    __tablename__ = "jornadas_san_jose"
    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(
        db.Integer,
        db.ForeignKey("temporadas_san_jose.id", ondelete="CASCADE"),
        nullable=False
    )
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship(
        "JosePartido",
        backref="jornada",
        cascade="all, delete-orphan"
    ) 

class JosePartido(db.Model):
    __tablename__ = 'san_jose_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_san_jose.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    puntosA = db.Column(db.String(225))
    puntosB = db.Column(db.String(225))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class JoseClub(db.Model):
    __tablename__ = 'san_jose_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffJose(db.Model):
    __tablename__ = 'playoff_san_jose'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer) 

class CopaJose(db.Model):
    __tablename__ = 'copa_san_jose'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer) 
    
class EuropaJose(db.Model):
    __tablename__ = 'europa_san_jose'
    id = db.Column(db.Integer, primary_key=True)
    encuentros = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer)

class Clasificacion(db.Model):
    __tablename__ = 'clasificacion_euro_san_jose'
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    equipo = db.Column(db.String(50))
    jugados = db.Column(db.Integer, default=0)
    ganados = db.Column(db.Integer, default=0)
    perdidos = db.Column(db.Integer, default=0)
    puntos = db.Column(db.Integer, default=0)    
    bonus = db.Column(db.Integer, default=0)  