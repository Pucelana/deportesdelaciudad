from flask import Blueprint
from app.routes.secciones import secciones_bp
from app.routes.resultados import resultados_bp

# Este archivo solo se encarga de importar los blueprints
# Puedes añadir aquí cualquier otro blueprint en el futuro

blueprints = [
    secciones_bp,
    resultados_bp,
]