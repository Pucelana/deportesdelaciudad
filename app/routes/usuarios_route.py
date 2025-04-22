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
@usuarios_route_bp.route('/register', methods=['POST'])
def register():
    nombre = request.form['usuario']
    email = request.form['email']
    password = request.form['password']
    # Verifica si ya existe ese usuario
    if Usuario.query.filter_by(email=email).first():
        # Aquí podrías usar flash para mostrar un mensaje en el modal
        return render_template('index.html')  # O donde tengas tu index
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    db.session.commit()
    login_user(nuevo_usuario)
    return render_template('index.html')  # Redirige a index tras login

# REGISTRO, LOGIN Y CIERRE DE SESIÓN USUARIOS
# Ruta de login
@usuarios_route_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')  # Recupera la redirección original
            return redirect(next_page or render_template('index.html'))
        else:
            return "Correo o contraseña incorrectos", 401
    return render_template ('index.html')

# Ruta de logout
@usuarios_route_bp.route('/logout')
@login_required
def logout():
    logout_user()  # Cierra la sesión del usuario
    return render_template ('index.html')  # Redirige a la página principal o donde desees

# Restringir acceso sin registro
@usuarios_route_bp.route('/perfil')
@login_required
def perfil():
    return render_template ('index.html')