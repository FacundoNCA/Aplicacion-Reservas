# import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class MyEnum(enum.Enum):
#     one = 1
#     two = 2
#     three = 3

class Clientes(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(24), nullable=False)

class Habitaciones(db.Model):
    __tablename__ = 'habitaciones'
    id_habitacion = db.Column(db.Integer, primary_key=True)
    tipo_habitacion = db.Column(db.String(36), default='basica')
    estado = db.Column(db.String(24), default='disponible')
    precio_noche = db.Column(db.Integer)
