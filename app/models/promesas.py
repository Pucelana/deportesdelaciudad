from app.extensions import db

class JornadaPromesas(db.Model):
    __tablename__ = 'jornada_promesas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('PromesasPartido', backref='jornada', cascade='all, delete-orphan')
    
class PromesasPartido(db.Model):
    __tablename__ = 'promesas_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornada_promesas.id'), nullable=False)
    fecha = db.Column(db.String(25))
    hora = db.Column(db.String(25))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)   

class PromesasClub(db.Model):
    __tablename__ = 'promesas_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)
    
class PlayoffPromesas(db.Model):
    __tablename__ = 'playoff_promesas'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer)