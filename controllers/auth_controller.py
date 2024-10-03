from functools import wraps

from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import User, db
from werkzeug.security import check_password_hash
from validators.user_forms import LoginForm, RegistrationForm


# Registro de nuevos usuarios
def register():
    form = RegistrationForm()  # Inicializa el formulario de registro
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Inicio de sesión
def login():
    form = LoginForm()  # Inicializa el formulario de inicio de sesión
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name  # Guardar nombre del usuario en la sesión
            flash('Has iniciado sesión exitosamente.')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


# Cerrar sesión
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Has cerrado sesión.')
    return redirect(url_for('login'))


# Proteger rutas (solo para usuarios autenticados)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Inicia sesión para acceder a esta página.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function
