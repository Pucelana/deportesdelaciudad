from app import create_app
from app.extensions import db
from app.models.horario import Horario
from app.models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC, Clasificacion, PlayoffUEMC
from app.models.valladolid import JornadaValladolid, ValladolidPartido, ValladolidClub, CopaValladolid,  PlayoffValladolid
from app.models.promesas import JornadaPromesas, PromesasPartido, PromesasClub,  PlayoffPromesas
from app.models.simancas import JornadaSimancas, SimancasPartido, SimancasClub, CopaSimancas,  PlayoffSimancas
from app.models.ponce import JornadaPonce, PoncePartido, PonceClub,  PlayoffPonce, Clasificacion
from app.models.aliados import JornadaAliados, AliadosPartido, AliadosClub,  PlayoffAliados, CopaAliados, SupercopaAliados, EurocupAliados, Clasificacion
from app.models.aula import JornadaAula, AulaPartido, AulaClub,  PlayoffAula, CopaAula, SupercopaIbericaAula, EuropaAula
from app.models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub,  PlayoffRecoletas, CopaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas, ClasificacionEuropa, CopaReyRecoletas
from app.models.caja import JornadaCaja, CajaPartido, CajaClub,  PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja, Clasificacion
from app.models.panteras import JornadaPanteras, PanterasPartido, PanterasClub,  PlayoffPanteras, CopaPanteras, SupercopaPanteras, EuropaPanteras, Clasificacion
from app.models.vrac import JornadaVrac, VracPartido, VracClub,  PlayoffVrac, CopaVrac, SupercopaIbericaVrac, EuropaVrac, Clasificacion
from app.models.galvan import JornadaGalvan, GalvanPartido, GalvanClub,  PlayoffGalvan, CopaGalvan
from app.models.usuarios import Usuario

from flask_login import LoginManager

app = create_app()

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['CACHE_TYPE'] = 'null'  # Esto desactiva el caché
app.debug = True

# --- FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.login_view = 'usuarios_route_bp.login'  # Nombre de la vista donde redirige si no está logueado
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id)) 


if __name__=="__main__":
    app.run(debug=True)

    