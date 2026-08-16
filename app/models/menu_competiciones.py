from app.extensions import db
from sqlalchemy import UniqueConstraint


class SeccionConfig(db.Model):
    __tablename__ = "secciones_config"

    id = db.Column(db.Integer, primary_key=True)

    # Clave interna de la sección
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    # Si la sección completa está visible
    activa = db.Column(db.Boolean, nullable=False, default=True)

    competiciones = db.relationship(
        "CompeticionConfig",
        back_populates="seccion",
        cascade="all, delete-orphan",
        lazy=True,
    )

    def __repr__(self):
        return f"<SeccionConfig {self.nombre}>"


class CompeticionConfig(db.Model):
    __tablename__ = "competiciones_config"

    id = db.Column(db.Integer, primary_key=True)

    # Relación con la sección
    seccion_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "secciones_config.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )

    # Ejemplo: liga, copa, playoff, europa...
    nombre = db.Column(db.String(100), nullable=False)

    # Si aparece en el menú
    activa = db.Column(db.Boolean, nullable=False, default=False)

    seccion = db.relationship(
        "SeccionConfig",
        back_populates="competiciones",
    )

    __table_args__ = (
        UniqueConstraint(
            "seccion_id",
            "nombre",
            name="uq_seccion_competicion",
        ),
    )

    def __repr__(self):
        return f"<CompeticionConfig {self.nombre}>"