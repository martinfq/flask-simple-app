from flask import Flask
from flask_wtf import CSRFProtect
from controllers import user_controller, auth_controller
from controllers.user_controller import edit_profile, delete_profile
from models.user_model import db
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)
db.init_app(app)

# Rutas
app.add_url_rule('/', view_func=user_controller.index)
app.add_url_rule('/register', view_func=auth_controller.register, methods=['GET', 'POST'])
app.add_url_rule('/login', view_func=auth_controller.login, methods=['GET', 'POST'])
app.add_url_rule('/logout', view_func=auth_controller.logout)
app.route('/edit_profile', methods=['GET', 'POST'])(edit_profile)
app.route('/delete_profile', methods=['POST'])(delete_profile)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
