from flask import Flask
from .extensions import db 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from .extensions import db
from .routes.secciones import secciones_bp
from .routes.resultados import resultados_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    app.register_blueprint(secciones_bp)
    app.register_blueprint(resultados_bp)
    
    return app 

    

    