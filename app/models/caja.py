from app.extensions import db

class JornadaCaja(db.Model):
    __tablename__ = 'jornadas_caja'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('CajaPartido', backref='jornada', cascade='all, delete-orphan')

class CajaPartido(db.Model):
    __tablename__ = 'caja_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_caja.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    bonusA = db.Column(db.String(120))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    bonusB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class CajaClub(db.Model):
    __tablename__ = 'caja_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffCaja(db.Model):
    __tablename__ = 'playoff_caja'
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

class CopaCaja(db.Model):
    __tablename__ = 'copa_caja'
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
    
class SupercopaCaja(db.Model):
    __tablename__ = 'supercopa_caja'
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

class EuropaCaja(db.Model):
    __tablename__ = 'europa_caja'
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