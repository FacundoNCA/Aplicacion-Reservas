import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    telefono = db.Column(db.String(24), nullable=False)
    contraseña = db.Column(db.Text, nullable=False)

class Habitaciones(db.Model):
    __tablename__ = 'habitaciones'
    id_habitacion = db.Column(db.Integer, primary_key=True)
    tipo_habitacion = db.Column(db.String(36), default='basica')
    disponible = db.Column(db.Boolean, default=True, nullable=False)
    precio_noche = db.Column(db.Integer)

class Reservas(db.Model):
    __tablename__ = 'reservas'
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    id_habitacion = db.Column(db.Integer, db.ForeignKey('habitaciones.id_habitacion'), nullable=False)
    fecha_llegada = db.Column(db.DateTime,  nullable=False)
    fecha_salida = db.Column(db.DateTime, nullable=False)
    metodo_pago = db.Column(db.String(20))
    monto = db.Column(db.Integer, nullable=False)
    pagado = db.Column(db.Boolean, default=False)

