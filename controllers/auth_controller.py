from functools import wraps

from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import User, db


# Registro de nuevos usuarios
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.')
            return redirect(url_for('register'))

        new_user = User(name=name, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.')
        return redirect(url_for('login'))

    return render_template('register.html')


# Inicio de sesión
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id  # Guardar el ID del usuario en la sesión
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas.')
            return redirect(url_for('login'))

    return render_template('login.html')


# Cerrar sesión
def logout():
    session.pop('user_id', None)  # Eliminar la sesión
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
