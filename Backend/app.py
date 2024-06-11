from flask import Flask 

app = Flask(__name__)

@app.route("/")
def get_shifts():
    return "<h1> Hola </h1>"
    

