from app.extensions import db

class TemporadaValladGenius(db.Model):
    __tablename__ = "temporadas_vallad_genius"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    activa = db.Column(db.Boolean, default=False)
    jornadas = db.relationship(
        "JornadaValladGenius",
        backref="temporada",
        cascade="all, delete-orphan"
    )
    
class JornadaValladGenius(db.Model):
    __tablename__ = "jornadas_vallad_genius"
    id = db.Column(db.Integer, primary_key=True)
    temporada_id = db.Column(
        db.Integer,
        db.ForeignKey("temporadas_vallad_genius.id", ondelete="CASCADE"),
        nullable=False
    )
    nombre = db.Column(db.String(255), nullable=False)
    partidos = db.relationship(
        "ValladGeniusPartido",
        backref="jornada",
        cascade="all, delete-orphan"
    )    
    
class ValladGeniusPartido(db.Model):
    __tablename__ = 'vallad_genius_partidos'
    id = db.Column(db.Integer, primary_key=True)
    jornada_id = db.Column(db.Integer, db.ForeignKey('jornadas_vallad_genius.id'), nullable=False)
    fecha = db.Column(db.String(25))
    hora = db.Column(db.String(25))
    local = db.Column(db.String(255))
    resultadoA = db.Column(db.String(120))
    resultadoB = db.Column(db.String(120))
    visitante = db.Column(db.String(255))
    orden = db.Column(db.Integer)   

class ValladGeniusClub(db.Model):
    __tablename__ = 'vallad_genius_clubs'
    # Definir la columna ID
    id = db.Column(db.Integer, primary_key=True)
    # Definir la columna 'nombre' para el nombre del club
    nombre = db.Column(db.String(255), nullable=False)
    
class ValladGeniusGrupo(db.Model):
    __tablename__ = "vallad_genius_grupos"

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(20), nullable=False)
    fase = db.Column(db.String(20), nullable=False)
    equipos = db.relationship(
        "ValladGeniusGrupoEquipo",
        backref="grupo",
        cascade="all, delete-orphan"
    )
    
class ValladGeniusGrupoEquipo(db.Model):
    __tablename__ = "vallad_genius_grupos_equipos"
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "vallad_genius_grupos.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    equipo = db.Column(
        db.String(255),
        nullable=False
    )    