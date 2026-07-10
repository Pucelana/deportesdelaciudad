from app import create_app
from app.extensions import db
from app.models.horario import Horario
from app.models.uemc import JornadaUEMC, UEMCPartido, UEMCClub, CopaUEMC, Clasificacion, PlayoffUEMC, TemporadaUEMC
from app.models.valladolid import JornadaValladolid, ValladolidPartido, ValladolidClub, CopaValladolid,  PlayoffValladolid, TemporadaValladolid, HistorialValladolid, Palmares
from app.models.promesas import JornadaPromesas, PromesasPartido, PromesasClub,  PlayoffPromesas, TemporadaPromesas
from app.models.simancas import JornadaSimancas, SimancasPartido, SimancasClub, CopaSimancas,  PlayoffSimancas, TemporadaSimancas
from app.models.parquesol import JornadaParquesol, ParquesolPartido, ParquesolClub, CopaParquesol,  PlayoffParquesol, TemporadaParquesol
from app.models.ponce import JornadaPonce, PoncePartido, PonceClub,  PlayoffPonce, Clasificacion, TemporadaPonce
from app.models.cdsi_vall import JornadaCDSIVall, CDSIVallPartido, CDSIVallClub,  PlayoffCDSIVall, Clasificacion, TemporadaCDSIVall
from app.models.aliados import JornadaAliados, AliadosPartido, AliadosClub,  PlayoffAliados, CopaAliados, SupercopaAliados, EurocupAliados, JornadaEurocup, TemporadaAliados
from app.models.aula import JornadaAula, AulaPartido, AulaClub,  PlayoffAula, CopaAula, SupercopaIbericaAula, EuropaAula, PermanenciaAula, JornadaPermanenciaAula, TemporadaAula
from app.models.recoletas import JornadaRecoletas, RecoletasPartido, RecoletasClub,  PlayoffRecoletas, CopaRecoletas, SupercopaIbericaRecoletas, EuropaRecoletas, ClasificacionEuropa, CopaReyRecoletas, TemporadaRecoletas
from app.models.caja import JornadaCaja, CajaPartido, CajaClub,  PlayoffCaja, CopaCaja, SupercopaCaja, EuropaCaja, Clasificacion, TemporadaCaja
from app.models.panteras import JornadaPanteras, PanterasPartido, PanterasClub,  PlayoffPanteras, CopaPanteras, SupercopaPanteras, EuropaPanteras, Clasificacion, TemporadaPanteras
from app.models.vrac import JornadaVrac, VracPartido, VracClub,  PlayoffVrac, CopaVrac, SupercopaIbericaVrac, EuropaVrac, Clasificacion, TemporadaVrac
from app.models.salvador import JornadaSalvador, SalvadorPartido, SalvadorClub,  PlayoffSalvador, CopaSalvador, SupercopaIbericaSalvador, EuropaSalvador, Clasificacion, TemporadaSalvador
from app.models.salvador_fem import JornadaSalvadorFem, SalvadorFemPartido, SalvadorFemClub,  PlayoffSalvadorFem, CopaSalvadorFem, SupercopaIbericaSalvadorFem, EuropaSalvadorFem, Clasificacion, TemporadaSalvadorFem
from app.models.galvan import JornadaGalvan, GalvanPartido, GalvanClub,  PlayoffGalvan, CopaGalvan, TemporadaGalvan
from app.models.vall_sala import JornadaVallSala, VallSalaPartido, VallSalaClub,  PlayoffVallSala, CopaVallSala, TemporadaVallSala
from app.models.vcv import JornadaVCV, VCVPartido, VCVClub,  PlayoffVCV, CopaVCV, EuropaVCV, Clasificacion, TemporadaVCV
from app.models.san_jose import JornadaJose, JosePartido, JoseClub,  PlayoffJose, CopaJose, EuropaJose, Clasificacion, TemporadaJose
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

    