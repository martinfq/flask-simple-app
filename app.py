from flask import Flask

from controllers import user_controller, auth_controller
from models.user_model import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)

# Rutas para usuarios (CRUD)
app.add_url_rule('/', view_func=user_controller.index)
# app.add_url_rule('/create', view_func=user_controller.create_user, methods=['GET', 'POST'])
# app.add_url_rule('/edit/<int:id>', view_func=user_controller.edit_user, methods=['GET', 'POST'])
# app.add_url_rule('/delete/<int:id>', view_func=user_controller.delete_user)

# Rutas para autenticación
app.add_url_rule('/register', view_func=auth_controller.register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=auth_controller.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=auth_controller.logout)

app.add_url_rule('/edit_profile', view_func=user_controller.edit_profile, methods=['GET', 'POST'])

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
