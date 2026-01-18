from flask import Blueprint, render_template

secciones_bp = Blueprint('secciones', __name__)

# Rutas de los equipos
@secciones_bp.route('/seccion/uemc')
def seccion_uemc():
    return render_template('secciones/uemc.html')

@secciones_bp.route('/seccion/ponce')
def seccion_ponce():
    return render_template('secciones/ponce.html')

@secciones_bp.route('/seccion/aliados')
def seccion_aliados():
    return render_template('secciones/aliados.html')

@secciones_bp.route('/seccion/aula')
def seccion_aula():
    return render_template('secciones/aula.html')

@secciones_bp.route('/seccion/recoletas')
def seccion_recoletas():
    return render_template('secciones/recoletas.html')

@secciones_bp.route('/seccion/valladolid')
def seccion_valladolid():
    return render_template('secciones/valladolid.html')

@secciones_bp.route('/seccion/promesas')
def seccion_promesas():
    return render_template('secciones/promesas.html')

@secciones_bp.route('/seccion/caja')
def seccion_caja():
    return render_template('secciones/caja.html')

@secciones_bp.route('/seccion/panteras')
def seccion_panteras():
    return render_template('secciones/panteras.html')

@secciones_bp.route('/seccion/vrac')
def seccion_vrac():
    return render_template('secciones/vrac.html')

@secciones_bp.route('/seccion/salvador')
def seccion_salvador():
    return render_template('secciones/salvador.html')

@secciones_bp.route('/seccion/univ')
def seccion_univ():
    return render_template('secciones/univ.html')

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