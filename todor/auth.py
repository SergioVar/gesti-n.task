from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from todor import db

# Creación del blueprint 'auth' para las rutas de autenticación
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Ruta para el registro de usuarios
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']
        
        # Crear nuevo usuario con la contraseña encriptada
        user = User(username, generate_password_hash(password))
        
        error = None
        
        # Comprobar si el usuario ya existe
        user_name = User.query.filter_by(username=username).first()
        if user_name is None:
            # Si el usuario no existe, agregar a la base de datos
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            # Si el usuario ya existe, mostrar un mensaje de error
            error = f'El usuario {username} ya está registrado'
        
        flash(error)
        
    return render_template('auth/register.html')

# Ruta para el inicio de sesión de usuarios
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        username = request.form['username']
        password = request.form['password']
        
        error = None
        
        # Validar los datos del usuario
        user = User.query.filter_by(username=username).first()
        if user is None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'
        
        # Iniciar sesión si no hay errores
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
        
        flash(error)
    return render_template('auth/login.html')

# Cargar el usuario registrado antes de cada petición
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

# Ruta para cerrar sesión
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

import functools

# Decorador para requerir inicio de sesión en vistas específicas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
