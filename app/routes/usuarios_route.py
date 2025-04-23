from flask import Blueprint, render_template, redirect, url_for, request, flash
from datetime import datetime
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from ..models.usuarios import Usuario  # Asegúrate de importar tu modelo Usuario
from app.extensions import db

usuarios_route_bp = Blueprint('usuarios_route_bp', __name__)

# Ruta de registro
@usuarios_route_bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('usuario')
        email = request.form.get('email')
        password = request.form.get('password')

        if Usuario.query.filter_by(email=email).first():
            flash('Este correo ya está registrado', 'warning')
            return redirect(url_for('resultados.sitio_home'))

        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()
        login_user(nuevo_usuario)

        flash('Registro exitoso. Sesión iniciada.', 'success')
        # Redirige a la página de "next" o a la home si no hay "next"
        next_page = request.args.get('next')
        if next_page:
            print("Next page:", next_page)
            return redirect(next_page or url_for('resultados.sitio_home'))
        return redirect(url_for('resultados.sitio_home'))

    return redirect(url_for('resultados.sitio_home'))  # Redirige a index tras login

# REGISTRO, LOGIN Y CIERRE DE SESIÓN USUARIOS
# Ruta de login
@usuarios_route_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            # Usamos current_user para verificar si el login fue exitoso
            if current_user.is_authenticated:
                flash('Has iniciado sesión con éxito.', 'success')
                next_page = request.args.get('next')
                print("Next page:", next_page)
                return redirect(next_page or url_for('resultados.sitio_home'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
            return redirect(url_for('resultados.sitio_home'))

    return redirect(url_for('resultados.sitio_home'))

# Ruta de logout
@usuarios_route_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Esto cierra la sesión del usuario
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('resultados.sitio_home'))  # Redirige a la página principal o donde desees

# Darse de baja
@usuarios_route_bp.route('/baja', methods=['POST'])
@login_required
def darse_de_baja():
    try:
        db.session.delete(current_user)
        db.session.commit()
        flash("Tu cuenta ha sido eliminada correctamente.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Ha ocurrido un error al intentar eliminar tu cuenta.", "danger")
    return redirect(url_for('resultados.sitio_home'))

# Restringir acceso sin registro
@usuarios_route_bp.route('/perfil')
@login_required
def perfil():
    return render_template ('index.html', usuario=current_user)

@usuarios_route_bp.route('/resultados')
@login_required
def resultados():
    # solo usuarios logueados pueden acceder a esta vista
    return render_template('index.html')