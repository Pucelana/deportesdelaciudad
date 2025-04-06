from app import create_app
from app.extensions import db
from app.models.horario import Horario



app = create_app()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_TYPE'] = 'null'  # Esto desactiva el caché
app.debug = True 

with app.app_context():
    db.create_all()




if __name__=="__main__":
    app.run(debug=True)

    