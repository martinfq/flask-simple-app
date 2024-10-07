from functools import wraps
from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import User, db
from werkzeug.security import check_password_hash
from validators.user_forms import LoginForm, RegistrationForm


# Función para el registro de nuevos usuarios
def register():
    form = RegistrationForm()  # Inicializa el formulario de registro
    if form.validate_on_submit():  # Verifica si el formulario es válido al enviar
        email = form.email.data  # Obtiene el email ingresado
        name = form.name.data  # Obtiene el nombre ingresado
        password = form.password.data  # Obtiene la contraseña ingresada

        # Verifica si el email ya está registrado en la base de datos
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.')  # Muestra mensaje de error
            return redirect(url_for('register'))  # Redirige al formulario de registro

        # Crea un nuevo usuario y establece la contraseña
        new_user = User(name=name, email=email)
        new_user.set_password(password)  # Hash de la contraseña

        db.session.add(new_user)  # Agrega el nuevo usuario a la sesión
        db.session.commit()  # Guarda los cambios en la base de datos
        flash('Registro exitoso. Ahora puedes iniciar sesión.')  # Mensaje de éxito
        return redirect(url_for('login'))  # Redirige a la página de inicio de sesión

    return render_template('register.html', form=form)  # Renderiza el formulario de registro


# Función para el inicio de sesión
def login():
    form = LoginForm()  # Inicializa el formulario de inicio de sesión
    if form.validate_on_submit():  # Verifica si el formulario es válido al enviar
        email = form.email.data  # Obtiene el email ingresado
        password = form.password.data  # Obtiene la contraseña ingresada

        # Verifica si el usuario existe y si la contraseña es correcta
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Valida la contraseña
            session['user_id'] = user.id  # Guarda el ID del usuario en la sesión
            session['user_name'] = user.name  # Guarda el nombre del usuario en la sesión
            flash('Has iniciado sesión exitosamente.')  # Mensaje de éxito
            return redirect(url_for('index'))  # Redirige al índice
        else:
            flash('Credenciales incorrectas.')  # Muestra mensaje de error
            return redirect(url_for('login'))  # Redirige al formulario de login

    return render_template('login.html', form=form)  # Renderiza el formulario de inicio de sesión


# Función para cerrar sesión
def logout():
    session.pop('user_id', None)  # Elimina el ID de usuario de la sesión
    session.pop('user_name', None)  # Elimina el nombre de usuario de la sesión
    flash('Has cerrado sesión.')  # Mensaje de cierre de sesión
    return redirect(url_for('login'))  # Redirige a la página de login


# Decorador para proteger rutas (solo usuarios autenticados)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si no hay usuario autenticado, redirige a la página de login
        if 'user_id' not in session:
            flash('Inicia sesión para acceder a esta página.')  # Mensaje de advertencia
            return redirect(url_for('login'))  # Redirige al formulario de login
        return f(*args, **kwargs)

    return decorated_function
