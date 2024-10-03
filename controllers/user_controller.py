from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import User, db
from controllers.auth_controller import login_required


def index():
    users = User.query.all()
    return render_template('index.html', users=users)


def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado exitosamente!')
        return redirect(url_for('index'))
    return render_template('create_user.html')


@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        flash('Usuario actualizado correctamente!')
        return redirect(url_for('index'))
    return render_template('create_user.html', user=user)


@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente!')
    return redirect(url_for('index'))
