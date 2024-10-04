from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from models.user_model import User, db
from controllers.auth_controller import login_required
from validators.user_forms import EditProfileForm, EmptyForm
from services.user_service import search_users
import re


def sanitize_input(input_string):
    """Sanitiza el input eliminando caracteres no deseados"""
    # Permitimos solo caracteres alfanuméricos y algunos de uso común como espacios.
    return re.sub(r'[^\w\s]', '', input_string)


def index():
    search_query = request.args.get('search', '').strip()

    # Validar si la cadena de búsqueda contiene caracteres válidos (ejemplo: alfanuméricos).
    if search_query:
        # Sanitizamos el input para evitar ataques XSS y otros.
        sanitized_query = sanitize_input(search_query)
        # También puedes escapar el input si lo vas a mostrar en algún lugar del frontend.
        escaped_query = escape(sanitized_query)
    else:
        escaped_query = ''

    # Obtener el número de página, asegurando que sea un entero
    page = request.args.get('page', 1, type=int)

    # Llamar a tu función de búsqueda usando la consulta sanitizada
    users = search_users(escaped_query, page, 5)

    return render_template('index.html', users=users, search_query=escaped_query)


@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    form = EditProfileForm(obj=user)

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                form.populate_obj(user)
                if form.password.data:  # Si hay nueva contraseña
                    user.set_password(form.password.data)

                db.session.commit()
                flash('Información actualizada exitosamente!')

                # Actualiza el nombre en la sesión si ha cambiado
                if user.name != session.get('user_name'):
                    session['user_name'] = user.name

                return redirect(url_for('edit_profile'))

            except Exception as e:
                db.session.rollback()
                flash('Ocurrió un error al actualizar los datos.')
                print(f"Error al guardar en la base de datos: {e}")

    return render_template('edit_profile.html', form=form, user=user)


@login_required
def delete_profile():
    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    form = EmptyForm()  # Crear un formulario simple solo para CSRF

    if request.method == 'POST' and form.validate_on_submit():
        try:
            db.session.delete(user)  # Elimina el usuario de la base de datos
            db.session.commit()  # Confirma los cambios
            session.clear()  # Limpia la sesión
            flash('Tu cuenta ha sido eliminada.')
            return redirect(url_for('register'))  # Redirige a la página de registro
        except Exception as e:
            db.session.rollback()
            flash('Ocurrió un error al eliminar la cuenta.')
            print(f"Error al eliminar la cuenta: {e}")

    return redirect(url_for('edit_profile'))
