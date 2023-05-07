from flask import Flask, jsonify, request, session
import json
from operator import itemgetter

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#logueo de usuario
@app.route('/login', methods=['POST'])
def login():
    datosLogin = request.get_json()
    if not "nombre" in datosLogin:
        return jsonify({"error": "no hay nombre en el login enviado"}), 400
    if not "contraseña" in datosLogin:
        return jsonify({"error": "no hay contraseña en el login enviado"}), 400
    with open("usuarios.json", "r", encoding="utf-8") as u:
        usuarios = json.load(u)
        for usuario in usuarios:
            if usuario["nombre"] == datosLogin["nombre"] and usuario["contraseña"] == datosLogin["contraseña"]:
                session["usuario"] = usuario["nombre"]
                return jsonify({"logueado": session["usuario"]}), 200
        return jsonify({"error": "no existe el usuario o la contraseña es incorrecta"}), 401
    
#registrar nuevo usuario
@app.route('/registro', methods=['POST'])
def registro():
    datosRegistro = request.get_json()
    if not "nombre" in datosRegistro:
        return jsonify({"error": "no hay nombre en el registro enviado"}), 400
    if not "contraseña" in datosRegistro:
        return jsonify({"error": "no hay contraseña en el registro enviado"}), 400
    with open("usuarios.json", "r", encoding="utf-8") as u:
        usuarios = json.load(u)
        for usuario in usuarios:
            if usuario["nombre"] == datosRegistro["nombre"]:
                return jsonify({"error": "ya existe un usuario con ese nombre"}), 400
        with open("usuarios.json", "w", encoding="utf-8") as u:
            usuarios.append(datosRegistro)
            json.dump(usuarios, u, ensure_ascii= False, indent=4)
            return jsonify({"usuario registrado": datosRegistro}), 200

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
@app.route("/peliculas/directores/<director>")
def peliculas_director(director):
    with open("peliculas.json", "r", encoding="utf-8") as peliculas:
        peliculas = json.load(peliculas)
        peliculas_director = []
        for pelicula in peliculas:
            if pelicula["director"] == director:
                peliculas_director.append(pelicula)
        return jsonify({"peliculas con mismo director": peliculas_director}), 200
    
#Endpoint peliculas con imagen
@app.route("/peliculas/imagen")
def peliculas_imagen():
    peliculasImagen = []
    with open("peliculas.json", "r", encoding="utf-8") as peliculas:
        peliculas = json.load(peliculas)
        for pelicula in peliculas:
            if pelicula["imagen"] != "":
                peliculasImagen.append(pelicula)
        return jsonify({"peliculas con imagen": peliculasImagen}), 200

#agregar nueva pelicula
@app.route("/pelicula", methods= ["POST"])
def nueva_pelicula():
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        peliculaNueva = request.get_json()
        if not "titulo" in peliculaNueva:
            return jsonify({"error": "no hay titulo en la pelicula enviada"}), 400
        if not "director" in peliculaNueva:
            return jsonify({"error": "no hay director en la pelicula enviada"}), 400
        if not "genero" in peliculaNueva:
            return jsonify({"error": "no hay genero en la pelicula enviada"}), 400
        if not "imagen" in peliculaNueva:
            return jsonify({"error": "no hay imagen en la pelicula enviada"}), 400
        if not "sinopsis" in peliculaNueva:
            return jsonify({"error": "no hay sinopsis en la pelicula enviada"}), 400
        with open("peliculas.json", "r", encoding="utf-8") as p:
            peliculas = json.load(p)
            #obtengo el id mas alto de las peliculas
            id = max(peliculas, key=itemgetter('id'))["id"] + 1
            nuevaPelicula = {"id": id, 
                            "titulo": peliculaNueva["titulo"], 
                            "director": peliculaNueva["director"], 
                            "genero": peliculaNueva["genero"], 
                            "imagen": peliculaNueva["imagen"], 
                            "sinopsis": peliculaNueva["sinopsis"]}
            peliculas.append(nuevaPelicula)
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, indent=4)
            return jsonify({"pelicula agregada": nuevaPelicula}), 200


#Endpoint de todas las peliculas del sistema
@app.route("/peliculas")
def peliculas():
    with open("peliculas.json", "r", encoding="utf-8") as peliculas:
        return jsonify({"peliculas":json.load(peliculas)}), 200


#modificar una pelicula
@app.route("/pelicula/<int:id>", methods= ["PUT"])
def modificar_pelicula(id):
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        editarPelicula = request.get_json()
        with open("peliculas.json", "r", encoding="utf-8") as p:
            peliculas = json.load(p)
            for pelicula in peliculas:
                if pelicula["id"] == id:
                    print(pelicula["id"])
                    if "titulo" in editarPelicula:
                        pelicula["titulo"] = editarPelicula["titulo"]
                    if "director" in editarPelicula:
                        pelicula["director"] = editarPelicula["director"]
                    if "genero" in editarPelicula:
                        pelicula["genero"] = editarPelicula["genero"]
                    if "imagen" in editarPelicula:
                        pelicula["imagen"] = editarPelicula["imagen"]
                    if "sinopsis" in editarPelicula:
                        pelicula["sinopsis"] = editarPelicula["sinopsis"]
                    print(pelicula)
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, indent=4)
        with open("peliculas.json", "r", encoding="utf-8") as p:
            peliculas = json.load(p) 
            for pelicula in peliculas:
                if pelicula["id"] == id:
                    return jsonify({"pelicula modificada": pelicula}), 200
                
#eliminar una pelicula
@app.route("/pelicula/<int:id>", methods= ["DELETE"])
def eliminar_pelicula(id):
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        with open("peliculas.json", "r", encoding="utf-8") as p:
            peliculas = json.load(p)
            for pelicula in peliculas:
                if pelicula["id"] == id:
                    peliculas.remove(pelicula)
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, indent=4)
            return jsonify({"pelicula eliminada": peliculas}), 200


if __name__ == "__main__": 
	app.run(debug = True, port=8000)
