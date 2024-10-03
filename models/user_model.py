from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    password = db.Column(db.String(200), nullable=False)  # Almacenará la contraseña encriptada

    # Método para establecer contraseña encriptada
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Método para verificar contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)
