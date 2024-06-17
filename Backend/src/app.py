from flask import Flask, render_template, request, jsonify
from models import db, Habitaciones, Clientes, Reservas
from flask_cors import CORS
import datetime


from config import config

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/app_reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ** RUTAS AUTHENTICATION CLIENTES  ----------------------------------------------------------------------------

@app.route("/auth/login", methods=["POST"])
def login_user():

    email = request.json.get("email")
    telefono = request.json.get("telefono")

    cliente = Clientes.query.where(( Clientes.email == email ) & (Clientes.telefono == telefono)).first()
    
    if ( cliente != None ):
        return jsonify({ "succes": True, "cliente": { "id_cliente": cliente.id_cliente, "nombre": cliente.nombre , "apellido": cliente.apellido, "email": cliente.email, "telefono": cliente.telefono} }), 200
    else:
        return jsonify({ "succes": False, "cliente": "user not-found"})
        

@app.route("/auth/register", methods=["POST"])
def register_user():

    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    email = request.json.get("email")
    telefono = request.json.get("telefono")

    nuevo_cliente = Clientes( nombre=nombre, apellido=apellido, email=email, telefono=telefono )
    db.session.add(nuevo_cliente)
    db.session.commit()

    return jsonify({ "succecs": "ok", "user": { "nombre": nombre, "apellido": apellido } })

# ** RUTAS PARA MANEJO DE DE HABITACIONES -------------------------------------------------------------------------------

@app.route("/")
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

@app.route("/", methods=["POST"])
def insertar_habitacion():

    tipo_habitacion = request.json.get("tipo_habitacion")
    disponible = request.json.get("disponible")
    precio_noche = request.json.get("precio_noche")

    nueva_habitacion = Habitaciones(tipo_habitacion=tipo_habitacion, disponible=disponible, precio_noche=precio_noche)
    db.session.add(nueva_habitacion)
    db.session.commit()
 
    return jsonify({ 'succes': True, "habitacion": { "tipo_habitacion": tipo_habitacion, "disponible": disponible, "precio_noche": precio_noche }  })

@app.route("/habitaciones")
def habitaciones():
    return render_template("index.html")

@app.route("/habitaciones/new")
def form_nueva_habitacion():
    habitaciones = get_habitaciones()
    return render_template('create_room.html')

# ** RUTAS PARA MANEJO DE DE RESERVAS -------------------------------------------------------------------------------

@app.route('/reservas')
def get_reservas():

    reservas = Reservas.query.all()
    reservas_data = []

    for r in reservas:
        reservas_data.append(r)

    return reservas_data

@app.route('/reservas', methods=["POST"])
def crear_reserva():

    email = request.json.get("email")
    tipo_habitacion = request.json.get("tipo_habitacion")
    cantidad_dias = request.json.get("cantidad_dias")
    # fecha_llegada = request.json.get("fecha_llegada")
    # fecha_salida = request.json.get("fecha_salida")

    cliente = Clientes.query.where(Clientes.email == email).first()
    habitacion = Habitaciones.query.where((Habitaciones.tipo_habitacion == tipo_habitacion) & (Habitaciones.disponible==True)).first()

    if ( habitacion != None ):
        id_cliente = cliente.id_cliente
        id_habitacion = habitacion.id_habitacion

        nueva_reserva = Reservas(id_cliente=id_cliente, id_habitacion=id_habitacion, fecha_salida=(datetime.datetime.now()+datetime.timedelta(days=cantidad_dias)))
        db.session.add(nueva_reserva)
        habitacion.disponible = False
        db.session.commit()
        return f"Hola { cliente.nombre } reserva hecha en la habitacion { id_habitacion }"
    else:
        return "No hay habitaciones disponibles"
    
@app.route('/reservas/<id_reserva>', methods=["DELETE"])
def cancelar_reserva(id_reserva):

    reserva = Reservas.query.where( Reservas.id_reserva == id_reserva ).first()

    if ( reserva != None ):
        habitacion = Habitaciones.query.where(Habitaciones.id_habitacion == reserva.id_habitacion).first()
        habitacion.disponible = True
        db.session.delete(reserva)
        db.session.commit()

        return jsonify({ "res_status": 200, "reserva": "cancelada" })
    else:
        return jsonify({ "res_status": 404, "reserva": "no encontrada"})




if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.config.from_object(config['development'])
    app.run()


    

