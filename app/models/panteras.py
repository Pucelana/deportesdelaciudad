from app.extensions import db

class JornadaPanteras(db.Model):
    __tablename__ = 'jornadas_panteras'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('PanterasPartido', backref='jornada', cascade='all, delete-orphan')

class PanterasPartido(db.Model):
    __tablename__ = 'panteras_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_panteras.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class PanterasClub(db.Model):
    __tablename__ = 'panteras_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffPanteras(db.Model):
    __tablename__ = 'playoff_panteras'
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

class CopaPanteras(db.Model):
    __tablename__ = 'copa_panteras'
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
    
class SupercopaPanteras(db.Model):
    __tablename__ = 'supercopa_panteras'
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

class EuropaPanteras(db.Model):
    __tablename__ = 'europa_panteras'
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
    __tablename__ = 'clasificacion_euro_panteras'
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    equipo = db.Column(db.String(50))
    jugados = db.Column(db.Integer, default=0)
    ganados = db.Column(db.Integer, default=0)
    perdidos = db.Column(db.Integer, default=0)
    puntos = db.Column(db.Integer, default=0)    
    bonus = db.Column(db.Integer, default=0)  