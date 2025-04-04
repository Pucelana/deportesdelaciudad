from ..extensions import db

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    deporte = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(10))  # masculino / femenino