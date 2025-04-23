from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .extensions import db
from .routes.secciones import secciones_bp
from .routes.resultados import resultados_bp
from .routes.uemc_route import uemc_route_bp
from .routes.valladolid_route import valladolid_route_bp
from .routes.promesas_route import promesas_route_bp
from .routes.simancas_route import simancas_route_bp
from .routes.ponce_route import ponce_route_bp
from .routes.aliados_route import aliados_route_bp
from .routes.aula_route import aula_route_bp
from .routes.recoletas_route import recoletas_route_bp
from .routes.usuarios_route import usuarios_route_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = 'sk_4F8v9u13sjd9sjd82018fh01hf01h'
    app.config.from_object('config.Config')
    db.init_app(app)
    from .models import uemc
    # Inicializa Flask-Migrate
    migrate = Migrate(app, db)
    app.register_blueprint(secciones_bp)
    app.register_blueprint(resultados_bp)
    app.register_blueprint(uemc_route_bp, url_prefix='/admin')
    app.register_blueprint(valladolid_route_bp, url_prefix='/admin')
    app.register_blueprint(promesas_route_bp, url_prefix='/admin')
    app.register_blueprint(simancas_route_bp, url_prefix='/admin')
    app.register_blueprint(ponce_route_bp, url_prefix='/admin')
    app.register_blueprint(aliados_route_bp, url_prefix='/admin')
    app.register_blueprint(aula_route_bp, url_prefix='/admin')
    app.register_blueprint(recoletas_route_bp, url_prefix='/admin')
    app.register_blueprint(usuarios_route_bp)
    
    return app 

    

    