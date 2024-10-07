from flask import render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from models.user_model import User, db
from controllers.auth_controller import login_required
from validators.user_forms import EditProfileForm, EmptyForm
from services.user_service import search_users
import re


# Función para sanitizar entradas eliminando caracteres no deseados
def sanitize_input(input_string):
    """Sanitiza el input eliminando caracteres no deseados."""
    # Permitimos solo caracteres alfanuméricos y algunos de uso común como espacios.
    return re.sub(r'[^\w\s]', '', input_string)


# Función principal que maneja la búsqueda de usuarios y muestra los resultados
def index():
    # Obtiene la cadena de búsqueda ingresada por el usuario, eliminando espacios extra
    search_query = request.args.get('search', '').strip()

    # Validar si la cadena de búsqueda contiene caracteres válidos (ejemplo: alfanuméricos)
    if search_query:
        # Sanitiza el input para evitar ataques XSS y otros
        sanitized_query = sanitize_input(search_query)
        # Escapa el input si se va a mostrar en el frontend
        escaped_query = escape(sanitized_query)
    else:
        escaped_query = ''  # Si no hay búsqueda, inicializa como cadena vacía

    # Obtener el número de página de los resultados, asegurando que sea un entero
    page = request.args.get('page', 1, type=int)

    # Llamar a la función de búsqueda utilizando la consulta sanitizada
    users = search_users(escaped_query, page, 5)  # Parámetros: búsqueda, página, y resultados por página

    # Renderiza la plantilla del índice con los usuarios encontrados y la búsqueda realizada
    return render_template('index.html', users=users, search_query=escaped_query)


# Función para editar el perfil del usuario autenticado
@login_required
def edit_profile():
    user_id = session.get('user_id')  # Obtiene el ID del usuario desde la sesión
    user = User.query.get_or_404(user_id)  # Busca al usuario o muestra error 404 si no existe
    form = EditProfileForm(obj=user)  # Inicializa el formulario con los datos del usuario

    if request.method == 'POST':  # Si el método de la solicitud es POST
        if form.validate_on_submit():  # Valida los datos del formulario
            try:
                form.populate_obj(user)  # Actualiza el objeto usuario con los datos del formulario
                if form.password.data:  # Si se ingresó una nueva contraseña
                    user.set_password(form.password.data)  # Actualiza la contraseña

                db.session.commit()  # Guarda los cambios en la base de datos
                flash('Información actualizada exitosamente!')

                # Actualiza el nombre del usuario en la sesión si ha cambiado
                if user.name != session.get('user_name'):
                    session['user_name'] = user.name

                return redirect(url_for('edit_profile'))  # Redirige a la misma página

            except Exception as e:
                db.session.rollback()  # Deshace los cambios si ocurre un error
                flash('Ocurrió un error al actualizar los datos.')
                print(f"Error al guardar en la base de datos: {e}")

    # Renderiza la plantilla para editar el perfil con el formulario y el usuario
    return render_template('edit_profile.html', form=form, user=user)


# Función para eliminar el perfil del usuario autenticado
@login_required
def delete_profile():
    user_id = session.get('user_id')  # Obtiene el ID del usuario desde la sesión
    user = User.query.get_or_404(user_id)  # Busca al usuario o muestra error 404 si no existe
    form = EmptyForm()  # Crea un formulario simple solo para validar CSRF

    # Si se envía el formulario con el método POST y es válido
    if request.method == 'POST' and form.validate_on_submit():
        try:
            db.session.delete(user)  # Elimina el usuario de la base de datos
            db.session.commit()  # Confirma los cambios
            session.clear()  # Limpia la sesión del usuario
            flash('Tu cuenta ha sido eliminada.')  # Muestra mensaje de éxito
            return redirect(url_for('register'))  # Redirige a la página de registro
        except Exception as e:
            db.session.rollback()  # Deshace los cambios si ocurre un error
            flash('Ocurrió un error al eliminar la cuenta.')
            print(f"Error al eliminar la cuenta: {e}")

    # Redirige a la página de editar perfil si no se envía correctamente el formulario
    return redirect(url_for('edit_profile'))
