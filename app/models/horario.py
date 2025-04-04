from app.extensions import db

class Horario(db.Model):
    __tablename__ = 'horarios'
    id = db.Column(db.Integer, primary_key=True)
    seccion = db.Column(db.String(100))
    liga = db.Column(db.String(100))
    equipoA = db.Column(db.String(100))
    resultado1 = db.Column(db.String(10))
    equipoB = db.Column(db.String(100))
    resultado2 = db.Column(db.String(10))
    fecha_partido = db.Column(db.String(50))
    def __repr__(self):
        return f'<Horario {self.equipoA} vs {self.equipoB} - {self.fecha_partido}>'