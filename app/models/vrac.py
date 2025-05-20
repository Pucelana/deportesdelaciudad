from app.extensions import db

class JornadaVrac(db.Model):
    __tablename__ = 'jornadas_vrac'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('VracPartido', backref='jornada', cascade='all, delete-orphan')

class VracPartido(db.Model):
    __tablename__ = 'vrac_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_vrac.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class VracClub(db.Model):
    __tablename__ = 'vrac_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffVrac(db.Model):
    __tablename__ = 'playoff_vrac'
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

class CopaVrac(db.Model):
    __tablename__ = 'copa_vrac'
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
    
class SupercopaIbericaVrac(db.Model):
    __tablename__ = 'supercopa_iberica_vrac'
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

class EuropaVrac(db.Model):
    __tablename__ = 'europa_vrac'
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
    __tablename__ = 'clasificacion_euro_vrac'
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    equipo = db.Column(db.String(50))
    jugados = db.Column(db.Integer, default=0)
    ganados = db.Column(db.Integer, default=0)
    perdidos = db.Column(db.Integer, default=0)
    puntos = db.Column(db.Integer, default=0)    
    bonus = db.Column(db.Integer, default=0)  