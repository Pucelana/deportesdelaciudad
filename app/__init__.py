from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .extensions import db, migrate
from .routes.secciones import secciones_bp
from .routes.resultados import resultados_bp
from .routes.uemc_route import uemc_route_bp
from .routes.valladolid_route import valladolid_route_bp
from .routes.promesas_route import promesas_route_bp
from .routes.simancas_route import simancas_route_bp
from .routes.parquesol_route import parquesol_route_bp
from .routes.ponce_route import ponce_route_bp
from .routes.cdsi_vall_route import cdsi_vall_route_bp
from .routes.aliados_route import aliados_route_bp
from .routes.aula_route import aula_route_bp
from .routes.recoletas_route import recoletas_route_bp
from .routes.caja_route import caja_route_bp
from .routes.panteras_route import panteras_route_bp
from .routes.vrac_route import vrac_route_bp
from .routes.galvan_route import galvan_route_bp
from .routes.vall_sala_route import vall_sala_route_bp
from .routes.salvador_route import salvador_route_bp
from .routes.salvador_fem_route import salvador_fem_route_bp
from .routes.vcv_route import vcv_route_bp
from .routes.usuarios_route import usuarios_route_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.secret_key = 'sk_4F8v9u13sjd9sjd82018fh01hf01h'
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .models import uemc

    app.register_blueprint(secciones_bp)
    app.register_blueprint(resultados_bp)
    app.register_blueprint(uemc_route_bp, url_prefix='/admin')
    app.register_blueprint(valladolid_route_bp, url_prefix='/admin')
    app.register_blueprint(promesas_route_bp, url_prefix='/admin')
    app.register_blueprint(simancas_route_bp, url_prefix='/admin')
    app.register_blueprint(parquesol_route_bp, url_prefix='/admin')
    app.register_blueprint(ponce_route_bp, url_prefix='/admin')
    app.register_blueprint(cdsi_vall_route_bp, url_prefix='/admin')
    app.register_blueprint(aliados_route_bp, url_prefix='/admin')
    app.register_blueprint(aula_route_bp, url_prefix='/admin')
    app.register_blueprint(recoletas_route_bp, url_prefix='/admin')
    app.register_blueprint(caja_route_bp, url_prefix='/admin')
    app.register_blueprint(panteras_route_bp, url_prefix='/admin')
    app.register_blueprint(vrac_route_bp, url_prefix='/admin')
    app.register_blueprint(galvan_route_bp, url_prefix='/admin')
    app.register_blueprint(vall_sala_route_bp, url_prefix='/admin')
    app.register_blueprint(salvador_route_bp, url_prefix='/admin')
    app.register_blueprint(salvador_fem_route_bp, url_prefix='/admin')
    app.register_blueprint(vcv_route_bp, url_prefix='/admin')
    app.register_blueprint(usuarios_route_bp)
    
    return app 

    

    