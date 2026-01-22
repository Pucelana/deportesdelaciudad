from app.extensions import db

class JornadaAliados(db.Model):
    __tablename__ = 'jornadas_aliados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('AliadosPartido', backref='jornada', cascade='all, delete-orphan')

class AliadosPartido(db.Model):
    __tablename__ = 'aliados_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_aliados.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)
      
class AliadosClub(db.Model):
    __tablename__ = 'aliados_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)

class PlayoffAliados(db.Model):
    __tablename__ = 'playoff_aliados'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer) 

class CopaAliados(db.Model):
    __tablename__ = 'copa_aliados'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer) 
    
class SupercopaAliados(db.Model):
    __tablename__ = 'supercopa_aliados'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(10), nullable=True)
    resultadoB = db.Column(db.String(10), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer)    

class EurocupAliados(db.Model):
    __tablename__ = 'eurocup_aliados'
    id = db.Column(db.Integer, primary_key=True)  # ID único para cada partido
    encuentros = db.Column(db.String(255), nullable=True)  # Encuentros, por ejemplo, nombre del torneo o fase
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))  # Hora del partido
    local = db.Column(db.String(255))  # Nombre del equipo local
    resultadoA = db.Column(db.String(120))  # Resultado del equipo local
    resultadoB = db.Column(db.String(120))  # Resultado del equipo visitante
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)      
    
class Clasificacion(db.Model):
    __tablename__ = 'clasificacion_eurocup'
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.String(50))
    equipo = db.Column(db.String(50))
    jugados = db.Column(db.Integer, default=0)
    ganados = db.Column(db.Integer, default=0)
    perdidos = db.Column(db.Integer, default=0)
    puntos = db.Column(db.Integer, default=0)        