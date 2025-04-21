from app import create_app
from app.extensions import db
from app.models.horario import Horario
from app.models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC, Clasificacion, PlayoffUEMC
from app.models.valladolid import JornadaValladolid, ValladolidPartido, ValladolidClub, CopaValladolid,  PlayoffValladolid
from app.models.promesas import JornadaPromesas, PromesasPartido, PromesasClub,  PlayoffPromesas
from app.models.simancas import JornadaSimancas, SimancasPartido, SimancasClub, CopaSimancas,  PlayoffSimancas
from app.models.ponce import JornadaPonce, PoncePartido, PonceClub,  PlayoffPonce
from app.models.aliados import JornadaAliados, AliadosPartido, AliadosClub,  PlayoffAliados, CopaAliados, SupercopaAliados
from app.models.aula import JornadaAula, AulaPartido, AulaClub,  PlayoffAula, CopaAula, SupercopaIbericaAula, EuropaAula
from app.models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub,  PlayoffRecoletas, CopaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas

app = create_app()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_TYPE'] = 'null'  # Esto desactiva el caché
app.debug = True 


if __name__=="__main__":
    app.run(debug=True)

    