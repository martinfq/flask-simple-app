from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user_model import db, User

user_bp = Blueprint('user_bp', __name__)

# Ruta principal - Listar usuarios
@user_bp.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

# Ruta para crear un nuevo usuario
@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente!')
        return redirect(url_for('user_bp.index'))
    return render_template('create_user.html')

# Ruta para editar un usuario existente
@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        flash('Usuario actualizado correctamente!')
        return redirect(url_for('user_bp.index'))
    return render_template('create_user.html', user=user)

# Ruta para eliminar un usuario
@user_bp.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente!')
    return redirect(url_for('user_bp.index'))
