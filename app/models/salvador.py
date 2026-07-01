from app.extensions import db

class TemporadaSalvador(db.Model):
    __tablename__ = "temporadas_salvador"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=False)
    jornadas = db.relationship(
        "JornadaSalvador",
        backref="temporada",
        cascade="all, delete-orphan"
    )
    
class JornadaSalvador(db.Model):
    __tablename__ = "jornadas_salvador"
    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(
        db.Integer,
        db.ForeignKey("temporadas_salvador.id", ondelete="CASCADE"),
        nullable=False
    )
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship(
        "SalvadorPartido",
        backref="jornada",
        cascade="all, delete-orphan"
    ) 

class SalvadorPartido(db.Model):
    __tablename__ = 'salvador_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_salvador.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class SalvadorClub(db.Model):
    __tablename__ = 'salvador_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffSalvador(db.Model):
    __tablename__ = 'playoff_salvador'
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

class CopaSalvador(db.Model):
    __tablename__ = 'copa_salvador'
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
    
class SupercopaIbericaSalvador(db.Model):
    __tablename__ = 'supercopa_iberica_salvador'
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

class EuropaSalvador(db.Model):
    __tablename__ = 'europa_salvador'
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
    __tablename__ = 'clasificacion_euro_salvador'
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    equipo = db.Column(db.String(50))
    jugados = db.Column(db.Integer, default=0)
    ganados = db.Column(db.Integer, default=0)
    perdidos = db.Column(db.Integer, default=0)
    puntos = db.Column(db.Integer, default=0)    
    bonus = db.Column(db.Integer, default=0)  