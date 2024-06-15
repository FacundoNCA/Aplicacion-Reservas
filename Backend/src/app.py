from flask import Flask, render_template, request, jsonify
from models import db, Habitaciones, Habitaciones
from sqlalchemy import insert
from flask_cors import CORS


from config import config

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/app_reservas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route("/")
def get_habitaciones():
    habitaciones = Habitaciones.query.all()

    habitaciones_data = []
    for h in habitaciones:

        habitacion = {
            "id_habitacion": h.id_habitacion,
            "tipo_habitacion": h.tipo_habitacion,
            "estado": h.estado,
            "precio_noche": h.precio_noche
        }

        habitaciones_data.append(habitacion)

    return habitaciones_data

@app.route("/", methods=["POST"])
def insertar_habitacion():

    tipo_habitacion = request.json.get("tipo_habitacion")
    estado = request.json.get("estado")
    precio_noche = request.json.get("precio_noche")

    nueva_habitacion = Habitaciones(tipo_habitacion=tipo_habitacion, estado=estado, precio_noche=precio_noche)
    db.session.add(nueva_habitacion)
    db.session.commit()
 
    return jsonify({ 'succes': True, "habitacion": { "tipo_habitacion": tipo_habitacion, "estado": estado, "precio_noche": precio_noche }  })

@app.route("/login")
def login():
    habitaciones = get_habitaciones()
    return render_template('login.html', habitaciones=habitaciones)

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.config.from_object(config['development'])
    app.run()


    

