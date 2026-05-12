from app.extensions import db

class JornadaAula(db.Model):
    __tablename__ = 'jornadas_aula'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship('AulaPartido', backref='jornada', cascade='all, delete-orphan')

class AulaPartido(db.Model):
    __tablename__ = 'aula_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_aula.id'), nullable=False)
    fecha = db.Column(db.String(20))
    hora = db.Column(db.String(20))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer, default=0)

class AulaClub(db.Model):
    __tablename__ = 'aula_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)
    
class JornadaPermanenciaAula(db.Model):
    __tablename__ = 'jornada_permanencia_aula'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    partidos = db.relationship(
        'PermanenciaAula',
        backref='jornada',
        lazy=True,
        cascade="all, delete-orphan"
    )    

class PermanenciaAula(db.Model):
    __tablename__ = 'permanencia_aula'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(
        db.Integer,
        db.ForeignKey('jornada_permanencia_aula.id')
    )
    fase = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(120), nullable=True)
    resultadoB = db.Column(db.String(120), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer, default=0)

class PlayoffAula(db.Model):
    __tablename__ = 'playoff_aula'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(120), nullable=True)
    resultadoB = db.Column(db.String(120), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer, default=0)

class CopaAula(db.Model):
    __tablename__ = 'copa_aula'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(120), nullable=True)
    resultadoB = db.Column(db.String(120), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer, default=0)
    
class SupercopaIbericaAula(db.Model):
    __tablename__ = 'supercopa_iberica_aula'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(120), nullable=True)
    resultadoB = db.Column(db.String(120), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer, default=0)

class EuropaAula(db.Model):
    __tablename__ = 'europa_aula'
    id = db.Column(db.Integer, primary_key=True)
    eliminatoria = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.String(20), nullable=True)
    hora = db.Column(db.String(10), nullable=True)
    local = db.Column(db.String(100), nullable=True)
    resultadoA = db.Column(db.String(120), nullable=True)
    resultadoB = db.Column(db.String(120), nullable=True)
    visitante = db.Column(db.String(100), nullable=True)
    orden = db.Column(db.Integer, default=0)          