from flask import Flask, jsonify, request, session
import json

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#logueo de usuario
@app.route('/login', methods=['POST'])
def login():
    #
    datosLogin = request.get_json()
    if not "nombre" in datosLogin:
        return jsonify({"error": "no hay nombre en el login enviado"}), 400
    if not "contraseña" in datosLogin:
        return jsonify({"error": "no hay contraseña en el login enviado"}), 400
    with open("usuarios.json", "r", encoding="utf-8") as u:
        usuarios = json.load(u)
        for usuario in usuarios:
            if usuario["nombre"] == datosLogin["nombre"] and usuario["contraseña"] == datosLogin["contraseña"]:
                session["username"] = usuario["nombre"]
                return jsonify({"logueado": session["username"]}), 200
        return jsonify({"error": "no existe el usuario o la contraseña es incorrecta"}), 401
    return ""

#ABM directores
@app.route("/directores")
def directores():
    with open("directores.json", "r", encoding="utf-8") as directores:
        return jsonify({"directores":json.load(directores)}), 200
    
#ABM géneros
@app.route("/generos")
def generos():
    with open("generos.json", "r", encoding="utf-8") as generos:
        return jsonify({"géneros":json.load(generos)}), 200
    
#Endpoint peliculas dirigidas por un director en particular
@app.route("/peliculas/directores/<director>" , methods= ["GET"])
def peliculas_mismo_director(director):
    if 'username' not in session:
        return jsonify({"error": "no estas logueado"}), 401
    else:
        salida = []
        if director in datos_sistema["directores"]:
            for pelicula in datos_sistema["peliculas"]:
                if director == pelicula["director"]:
                    salida.append(pelicula)
            return jsonify({f"peliculas dirigidas por {director}": salida}), 200


if __name__ == "__main__": 
	app.run(debug = True, port=8000)
