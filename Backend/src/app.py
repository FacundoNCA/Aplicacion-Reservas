from flask import Flask, request, jsonify
from models import db, Habitaciones, Clientes, Reservas
from flask_cors import CORS
from jwt import exceptions
import datetime
import jwt

from config import config

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/app_reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# TODO: AGREGAR UN ARCHIVO .ENV Y PONER SECRET_KEY COMO VARIABLE DE ENTORNO

SECRET_KEY = "aguanteboca"

# ** RUTAS AUTHENTICATION CLIENTES  ----------------------------------------------------------------------------

@app.route("/auth/login", methods=["POST"])
def login_user():

    email = request.json.get("email")
    contraseña = request.json.get("contraseña")

    cliente = Clientes.query.where(( Clientes.email == email ) & (Clientes.contraseña == contraseña)).first()

    if ( cliente != None ):

        tokenPayload = {
            "id_cliente": cliente.id_cliente,
            "nombre": cliente.nombre,
            "apellido": cliente.apellido,
            "email": cliente.email,
            "contraseña": cliente.contraseña,
        }

        encoded = jwt.encode(tokenPayload, SECRET_KEY, algorithm="HS256")
        return jsonify({ "succes": True, "token": encoded }), 200
    else:
        return jsonify({ "succes": False, "cliente": "user not-found"}), 404
        

@app.route("/auth/register", methods=["POST"])
def register_user():

    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    email = request.json.get("email")
    contraseña = request.json.get("contraseña")
    telefono = request.json.get("telefono")

    cliente = Clientes.query.where( Clientes.email == email ).first()

    if ( cliente == None ):
        nuevo_cliente = Clientes( nombre=nombre, apellido=apellido, email=email, contraseña=contraseña, telefono=telefono )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return jsonify({ "succecs": True, "user": "created" }), 201
    else:
        return jsonify({ "succecs": False, "user": "already exist" })

    

# ** RUTAS PARA MANEJO DE DE HABITACIONES -------------------------------------------------------------------------------

@app.route("/habitaciones")
def get_habitaciones():
    habitaciones = Habitaciones.query.all()

    habitaciones_data = []
    for h in habitaciones:

        habitacion = {
            "id_habitacion": h.id_habitacion,
            "tipo_habitacion": h.tipo_habitacion,
            "disponible": h.disponible,
            "precio_noche": h.precio_noche
        }

        habitaciones_data.append(habitacion)

    return habitaciones_data

@app.route("/habitaciones", methods=["POST"])
def insertar_habitacion():

    tipo_habitacion = request.json.get("tipo_habitacion")
    precio_noche = request.json.get("precio_noche")

    nueva_habitacion = Habitaciones(tipo_habitacion=tipo_habitacion, precio_noche=precio_noche)
    db.session.add(nueva_habitacion)
    db.session.commit()
 
    return jsonify({ 'succes': True, "habitacion": { "tipo_habitacion": tipo_habitacion, "precio_noche": precio_noche }  })


# ** RUTAS PARA MANEJO DE DE RESERVAS -------------------------------------------------------------------------------

@app.route('/reservas')
def get_reservas():

    reservas = Reservas.query.all()
    reservas_data = []

    for r in reservas:

        reserva = {
            "id_reserva": r.id_reserva,
            "id_cliente": r.id_cliente,
            "id_habitacion": r.id_habitacion,
            "fecha_llegada": r.fecha_llegada,
            "fecha_salida": r.fecha_salida,
            "metodo_pago": r.metodo_pago,
            "monto": r.monto,
            "pagado": r.pagado
        }

        reservas_data.append(reserva)

    return reservas_data

@app.route('/reservas/personal')
def get_reservasByCliente():

    try:
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return jsonify({"message": "Falta token de autenticación"}), 401
        
        token = request.headers['Authorization'].split(' ')[1]
        usuario = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        id_cliente = usuario["id_cliente"]
    except exceptions.DecodeError:
        return jsonify({ "message": "invalid token" })

    reservas = Reservas.query.where(Reservas.id_cliente == id_cliente).all()
    reservas_data = []
    for r in reservas:
        reserva = {
            "id_reserva": r.id_reserva,
            "id_cliente": r.id_cliente,
            "id_habitacion": r.id_habitacion,
            "fecha_llegada": r.fecha_llegada,
            "fecha_salida": r.fecha_salida,
            "metodo_pago": r.metodo_pago,
            "monto": r.monto,
            "pagado": r.pagado
        }

        reservas_data.append(reserva)

    return reservas_data

@app.route('/reservas', methods=["POST"])
def crear_reserva():

    try:
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return jsonify({"message": "missing authorization header"}), 401

        token = request.headers['Authorization'].split(' ')[1]
        usuario = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        email = usuario["email"]
    except exceptions.DecodeError:
        return jsonify({ "message": "invalid token" })


    tipo_habitacion = request.json.get("tipo_habitacion")
    fecha_llegada_str = request.json.get("fecha_llegada")
    fecha_salida_str = request.json.get("fecha_salida")
    metodo_pago = request.json.get("metodo_pago")


    fecha_llegada = datetime.datetime.strptime(fecha_llegada_str, '%d/%m/%Y')
    fecha_salida = datetime.datetime.strptime(fecha_salida_str, '%d/%m/%Y')

    cantidad_dias = (fecha_salida - fecha_llegada).days

    cliente = Clientes.query.where(Clientes.email == email).first()
    habitacion = Habitaciones.query.where((Habitaciones.tipo_habitacion == tipo_habitacion) & (Habitaciones.disponible==True)).first()

    if ( habitacion != None ):
        id_cliente = cliente.id_cliente
        id_habitacion = habitacion.id_habitacion
        nueva_reserva = Reservas(
                id_cliente=id_cliente,
                id_habitacion=id_habitacion,
                fecha_llegada=fecha_llegada,
                fecha_salida=fecha_salida,
                metodo_pago=metodo_pago,
                monto=(habitacion.precio_noche * cantidad_dias)
            )
        
        db.session.add(nueva_reserva)
        habitacion.disponible = False
        db.session.commit()

        return jsonify({ "succes": True, "room": id_habitacion }), 200
    else:
        return jsonify({ "succes": False, "room": habitacion }), 503

@app.route("/reservas/<id_reserva>", methods=["PUT"])
def pagar_reserva(id_reserva):

    metodo_pago = request.json.get("metodo_pago")

    reserva = Reservas.query.where(Reservas.id_reserva == id_reserva).first()

    if ( reserva != None ):
        reserva.pagado = True
        reserva.metodo_pago = metodo_pago
        db.session.commit()

    return jsonify({ "reserva": "pagada", "monto": reserva.monto })

@app.route('/reservas/<id_reserva>', methods=["DELETE"])
def cancelar_reserva(id_reserva):

    reserva = Reservas.query.where( Reservas.id_reserva == id_reserva ).first()

    if ( reserva != None ):
        habitacion = Habitaciones.query.where(Habitaciones.id_habitacion == reserva.id_habitacion).first()
        habitacion.disponible = True
        db.session.delete(reserva)
        db.session.commit()

        return jsonify({ "res_status": 200, "reserva": "cancelada" }), 200
    else:
        return jsonify({ "res_status": 404, "reserva": "no encontrada"}), 404


if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.config.from_object(config['development'])
    app.run()


    

