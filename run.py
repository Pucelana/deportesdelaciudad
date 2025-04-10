from app import create_app
from app.extensions import db
from app.models.horario import Horario
from app.models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC, Clasificacion, PlayoffUEMC
from app.models.valladolid import JornadaValladolid, ValladolidPartido, ValladolidClub, CopaValladolid, ClasifValladolid, PlayoffValladolid

app = create_app()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_TYPE'] = 'null'  # Esto desactiva el caché
app.debug = True 


if __name__=="__main__":
    app.run(debug=True)

    