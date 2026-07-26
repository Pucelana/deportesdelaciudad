from flask import Blueprint, render_template
from app.models.comercial import COMERCIAL

secciones_bp = Blueprint('secciones', __name__)

def render_seccion(template, nombre, zona='seccion'):
    comercial = COMERCIAL.get(nombre, {})

    return render_template(
        template,
        comercial=comercial,
        zona=zona
    )

# Rutas de los equipos
@secciones_bp.route('/seccion/uemc')
def seccion_uemc():
    return render_seccion('secciones/uemc.html', 'uemc')

@secciones_bp.route('/seccion/ponce')
def seccion_ponce():
    return render_seccion('secciones/ponce.html', 'ponce')

@secciones_bp.route('/seccion/cdsi_vall')
def seccion_cdsi_vall():
    return render_seccion('secciones/cdsi_vall.html', 'vall_sala')

@secciones_bp.route('/seccion/vcv')
def seccion_vcv():
    return render_seccion('secciones/vcv.html', 'vcv')

@secciones_bp.route('/seccion/san_jose')
def seccion_san_jose():
    return render_seccion('secciones/san_jose.html', 'san_jose')

@secciones_bp.route('/seccion/aliados')
def seccion_aliados():
    return render_seccion('secciones/aliados.html', 'aliados')

@secciones_bp.route('/seccion/aula')
def seccion_aula():
    return render_seccion('secciones/aula.html', 'aula')

@secciones_bp.route('/seccion/recoletas')
def seccion_recoletas():
    return render_seccion('secciones/recoletas.html', 'recoletas')

@secciones_bp.route('/seccion/valladolid')
def seccion_valladolid():
    return render_seccion('secciones/valladolid.html', 'valladolid')

@secciones_bp.route('/seccion/promesas')
def seccion_promesas():
    return render_seccion('secciones/promesas.html', 'promesas')

@secciones_bp.route('/seccion/caja')
def seccion_caja():
    return render_seccion('secciones/caja.html', 'caja')

@secciones_bp.route('/seccion/panteras')
def seccion_panteras():
    return render_seccion('secciones/panteras.html', 'panteras')

@secciones_bp.route('/seccion/vrac')
def seccion_vrac():
    return render_seccion('secciones/vrac.html', 'vrac')

@secciones_bp.route('/seccion/salvador')
def seccion_salvador():
    return render_seccion('secciones/salvador.html', 'salvador')

@secciones_bp.route('/seccion/salvador_fem')
def seccion_salvador_fem():
    return render_seccion('secciones/salvador_fem.html', 'salvador_fem')

@secciones_bp.route('/seccion/rv_femenino')
def seccion_rv_femenino():
    return render_seccion('secciones/rv_femenino.html', 'rv_femenino')

@secciones_bp.route('/seccion/parquesol')
def seccion_parquesol():
    return render_seccion('secciones/parquesol.html', 'parquesol')

@secciones_bp.route('/seccion/galvan')
def seccion_galvan():
    return render_seccion('secciones/galvan.html', 'galvan')

@secciones_bp.route('/seccion/vall_sala')
def seccion_vall_sala():
    return render_template('secciones/vall_sala.html', 'vall_sala')

# Rutas de sistemas de ligas
@secciones_bp.route('/sistema_ligas/futbol')
def sistema_ligas_futbol():
    return render_template('sistema_ligas/sistema_futbol.html')

@secciones_bp.route('/sistema_ligas/baloncesto')
def sistema_ligas_baloncesto():
    return render_template('sistema_ligas/sistema_baloncesto.html')

@secciones_bp.route('/sistema_ligas/balonmano')
def sistema_ligas_balonmano():
    return render_template('sistema_ligas/sistema_balonmano.html')

@secciones_bp.route('/sistema_ligas/rugby')
def sistema_ligas_rugby():
    return render_template('sistema_ligas/sistema_rugby.html')

@secciones_bp.route('/sistema_ligas/hockey')
def sistema_ligas_hockey():
    return render_template('sistema_ligas/sistema_hockey.html')

@secciones_bp.route('/sistema_ligas/futbol_sala')
def sistema_ligas_futbol_sala():
    return render_template('sistema_ligas/sistema_futbol_sala.html')

@secciones_bp.route('/sistema_ligas/voleibol')
def sistema_ligas_voleibol():
    return render_template('sistema_ligas/sistema_voleibol.html')