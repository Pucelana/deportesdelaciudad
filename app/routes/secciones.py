from flask import Blueprint, render_template

secciones_bp = Blueprint('secciones', __name__)

# Rutas de secciones deportivas
@secciones_bp.route('/seccion/baloncesto')
def seccion_baloncesto():
    return render_template('secciones/baloncesto.html')

@secciones_bp.route('/seccion/balonmano')
def seccion_balonmano():
    return render_template('secciones/balonmano.html')

@secciones_bp.route('/seccion/futbol')
def seccion_futbol():
    return render_template('secciones/futbol.html')

@secciones_bp.route('/seccion/futbol_sala')
def seccion_futbol_sala():
    return render_template('secciones/futbol_sala.html')

@secciones_bp.route('/seccion/hockey')
def seccion_hockey():
    return render_template('secciones/hockey.html')

@secciones_bp.route('/seccion/rugby')
def seccion_rugby():
    return render_template('secciones/rugby.html')

@secciones_bp.route('/seccion/voleibol')
def seccion_voleibol():
    return render_template('secciones/voleibol.html')

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