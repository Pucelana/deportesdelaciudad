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
from .routes.rv_fem_route import rv_fem_route_bp
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
from .routes.vallad_genius_route import vallad_genius_route_bp
from .routes.salvador_route import salvador_route_bp
from .routes.salvador_fem_route import salvador_fem_route_bp
from .routes.vcv_route import vcv_route_bp
from .routes.san_jose_route import san_jose_route_bp
from .seo.sitemap_index import sitemap_index_bp
from .seo.sitemap_general import sitemap_general_bp
from .seo.sitemap_baloncesto import sitemap_baloncesto_bp
from .seo.sitemap_futbol import sitemap_futbol_bp
from .seo.sitemap_futsal import sitemap_futsal_bp
from .seo.sitemap_balonmano import sitemap_balonmano_bp
from .seo.sitemap_rugby import sitemap_rugby_bp
from .seo.sitemap_hockey import sitemap_hockey_bp
from .seo.sitemap_voley import sitemap_voley_bp
from .seo.sitemap_copa import sitemap_copa_bp
from .seo.sitemap_europa import sitemap_europa_bp
from .seo.sitemap_playoff import sitemap_playoff_bp
from .seo.sitemap_historial import sitemap_historial_bp
from .routes.usuarios_route import usuarios_route_bp
from .routes.seo_routes import seo_bp
from app.seo.social import SOCIAL
from .routes.menu_competiciones_route import menu_competiciones_bp
from app.utils.sincronizar_menu import sincronizar_menu_competiciones
from .seo.sitemap_index import sitemap_index_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    
    @app.context_processor
    def inject_schema():
        from .seo.schema import schema_website, jsonld
        return {
            "schema_web": jsonld(schema_website())
        }
    
    @app.context_processor
    def inject_social():
        return dict(SOCIAL=SOCIAL)    
    
    app.secret_key = os.environ.get("SECRET_KEY")
    app.config.from_object('config.Config')
    
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
    
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        sincronizar_menu_competiciones()
    
    from .models import uemc
    from .models import menu_competiciones

    app.register_blueprint(secciones_bp)
    app.register_blueprint(resultados_bp)
    app.register_blueprint(uemc_route_bp)
    app.register_blueprint(valladolid_route_bp)
    app.register_blueprint(promesas_route_bp)
    app.register_blueprint(rv_fem_route_bp)
    app.register_blueprint(parquesol_route_bp)
    app.register_blueprint(ponce_route_bp)
    app.register_blueprint(cdsi_vall_route_bp)
    app.register_blueprint(aliados_route_bp)
    app.register_blueprint(aula_route_bp)
    app.register_blueprint(recoletas_route_bp)
    app.register_blueprint(caja_route_bp)
    app.register_blueprint(panteras_route_bp)
    app.register_blueprint(vrac_route_bp)
    app.register_blueprint(galvan_route_bp)
    app.register_blueprint(vall_sala_route_bp)
    app.register_blueprint(vallad_genius_route_bp)
    app.register_blueprint(salvador_route_bp)
    app.register_blueprint(salvador_fem_route_bp)
    app.register_blueprint(vcv_route_bp)
    app.register_blueprint(san_jose_route_bp)
    app.register_blueprint(sitemap_index_bp)
    app.register_blueprint(sitemap_general_bp)
    app.register_blueprint(sitemap_baloncesto_bp)
    app.register_blueprint(sitemap_futbol_bp)
    app.register_blueprint(sitemap_futsal_bp)
    app.register_blueprint(sitemap_balonmano_bp)
    app.register_blueprint(sitemap_rugby_bp)
    app.register_blueprint(sitemap_hockey_bp)
    app.register_blueprint(sitemap_voley_bp)
    app.register_blueprint(sitemap_copa_bp)
    app.register_blueprint(sitemap_europa_bp)
    app.register_blueprint(sitemap_playoff_bp)
    app.register_blueprint(sitemap_historial_bp)
    app.register_blueprint(usuarios_route_bp)
    app.register_blueprint(seo_bp)
    app.register_blueprint(menu_competiciones_bp)
    print("\n========== RUTAS REGISTRADAS ==========\n")

    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.rule):
        print(f"{rule.endpoint:50} -> {rule.rule}")

        print("\n=======================================\n")
    
    return app 