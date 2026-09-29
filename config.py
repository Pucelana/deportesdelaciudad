import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    uri = os.environ.get('DATABASE_URL')
    
    if not uri:
        raise ValueError("DATABASE_URL no está definida")

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)
    elif uri and uri.startswith("postgresql://"):
        uri = uri.replace("postgresql://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = uri   
    