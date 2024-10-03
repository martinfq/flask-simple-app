from flask import render_template, request, redirect, url_for, flash, session
from models.user_model import User, db
from controllers.auth_controller import login_required


def index():
    search_query = request.args.get('search')  # Obtener el término de búsqueda de la URL

    if search_query:
        # Filtrar usuarios cuyo nombre o correo coincidan con el término de búsqueda
        users = User.query.filter(
            (User.name.ilike(f"%{search_query}%")) | (User.email.ilike(f"%{search_query}%"))
        ).all()
    else:
        # Si no hay término de búsqueda, mostrar todos los usuarios
        users = User.query.all()

    return render_template('index.html', users=users, search_query=search_query)


@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        if 'update' in request.form:
            user.name = request.form['name']
            user.email = request.form['email']
            if request.form['password']:
                user.set_password(request.form['password'])
            db.session.commit()
            flash('Información actualizada exitosamente!')
            return redirect(url_for('edit_profile'))

        elif 'delete' in request.form:  # Si se presiona el botón "Eliminar cuenta"
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)  # Elimina al usuario de la sesión
            flash('Tu cuenta ha sido eliminada.')
            return redirect(url_for('register'))

    return render_template('edit_profile.html', user=user)
