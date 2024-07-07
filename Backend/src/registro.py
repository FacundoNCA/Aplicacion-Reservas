from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='Aplicacion-Reservas/Frontend')  # Define el directorio de plantillas
CORS(app)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adrian:12345@localhost/usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'credenciales'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(120), nullable=False)

# Ruta para el registro de usuarios
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    contrasena = data.get('contrasena')

    # Verificar si el usuario ya existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'message': 'El correo ya está registrado'}), 400

    # Crear un nuevo usuario
    nuevo_usuario = Usuario(email=email, contrasena=contrasena)
    db.session.add(nuevo_usuario)
    db.session.commit()

    # Redirigir a la página de registro si el registro es exitoso
    return jsonify({'message': 'Registro exitoso', 'redirect_url': '/Registro.html'}), 200

# Ruta para el inicio de sesión de usuarios
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    contrasena = data.get('contrasena')

    # Verificar si el usuario existe y la contraseña es correcta
    usuario = Usuario.query.filter_by(email=email, contrasena=contrasena).first()
    if usuario:
        # Crear un token (opcional) y almacenar en la sesión (si no se usa JWT)
        session['user_id'] = usuario.id
        return jsonify({'message': 'Inicio de sesión exitoso', 'redirect_url': '/Reservas.html'}), 200
    else:
        return jsonify({'message': 'Correo o contraseña incorrectos'}), 401

# Ruta para la página principal (Pagina_p.html)
@app.route('/')
def index():
    return render_template('Pagina_p.html')

# Ruta para Registro.html
@app.route('/Registro.html')
def registro():
    return render_template('Registro.html')

if __name__ == '__main__':
    app.run(debug=True)
