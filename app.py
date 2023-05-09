from flask import Flask, jsonify, request, session
import json
from operator import itemgetter
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
CORS(app)


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
                session["permiso"] = usuario["permiso"]
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
            usuarios.append({"nombre": datosRegistro["nombre"], 
                             "contraseña": datosRegistro["contraseña"],
                             "permiso": "usuario"})
            json.dump(usuarios, u, ensure_ascii= False, indent=4)
            return jsonify({"usuario registrado": datosRegistro["nombre"]}), 200
        
#editar usuario
@app.route('/usuario', methods=['PUT'])
def editar_usuario():
    if not "usuario" in session:
        return jsonify({"error": "no estas logueado"}), 401
    else:
        datosUsuario = request.get_json()
        with open("usuarios.json", "r", encoding="utf-8") as u:
            usuarios = json.load(u)
            for usuario in usuarios:
                if usuario["nombre"] == session["usuario"]:
                    if "nombre" in datosUsuario:
                        usuario["nombre"] = datosUsuario["nombre"]
                        session["usuario"] = usuario["nombre"]
                    if "contraseña" in datosUsuario:
                        usuario["contraseña"] = datosUsuario["contraseña"]
        with open("usuarios.json", "w", encoding="utf-8") as u:
            json.dump(usuarios, u, ensure_ascii= False, indent=4)
            return jsonify({"usuario editado": session["usuario"]}), 200
        
#ABM directores
@app.route("/directores")
@app.route("/directores/<director>", methods=["POST", "DELETE"])
def directores(director=None):
    if not "usuario" in session:
        return jsonify({"error": "no estas logueado"}), 401
    else:
        if request.method == "GET":
            with open("directores.json", "r", encoding="utf-8") as directores:
                return jsonify({"directores del sistema":json.load(directores)}), 200
        if request.method == "POST":
            if session["permiso"] == "admin":
                if not director:
                    return jsonify({"error": "no hay director en el parametro enviado"}), 400
                with open("directores.json", "r", encoding="utf-8") as d:
                    directores = json.load(d)
                    for d in directores:
                        if d == director:
                            return jsonify({"error": "ya existe ese director"}), 400
                    with open("directores.json", "w", encoding="utf-8") as d:
                        directores.append(director)
                        json.dump(directores, d, ensure_ascii= False, indent=4)
                        return jsonify({"director agregado": director}), 200
            else:
                return jsonify({"error": "necesitas permiso de admin para agregar un director"}), 403
        if request.method == "DELETE":
            if session["permiso"] == "admin":
                if not director:
                    return jsonify({"error": "no hay director en el parametro enviado"}), 400
                with open("directores.json", "r", encoding="utf-8") as d:
                    directores = json.load(d)
                    for d in directores:
                        if d == director:
                            directores.remove(d)
                            with open("directores.json", "w", encoding="utf-8") as d:
                                json.dump(directores, d, ensure_ascii= False, indent=4)
                                return jsonify({"director eliminado": director}), 200
                    return jsonify({"error": "no existe ese director"}), 400
            else:
                return jsonify({"error": "necesitas permiso de admin para eliminar un director"}), 403

    
    
#ABM géneros
@app.route("/generos")
@app.route("/generos/<genero>", methods=["POST", "DELETE"])
def generos(genero=None):
    if not "usuario" in session:
        return jsonify({"error": "no estas logueado"}), 401
    else:
        if request.method == "GET":
            with open("generos.json", "r", encoding="utf-8") as generos:
                return jsonify({"generos del sistema":json.load(generos)}), 200
        if request.method == "POST":
            if session["permiso"] == "admin":
                if not genero:
                    return jsonify({"error": "no hay genero en el parametro enviado"}), 400
                with open("generos.json", "r", encoding="utf-8") as g:
                    generos = json.load(g)
                    for g in generos:
                        if g == genero:
                            return jsonify({"error": "ya existe ese genero"}), 400
                    with open("generos.json", "w", encoding="utf-8") as g:
                        generos.append(genero)
                        json.dump(generos, g, ensure_ascii= False, indent=4)
                        return jsonify({"genero agregado": genero}), 200
            else:
                return jsonify({"error": "necesitas permiso de admin para agregar un genero"}), 403
        if request.method == "DELETE":
            if session["permiso"] == "admin":
                if not genero:
                    return jsonify({"error": "no hay genero en el parametro enviado"}), 400
                with open("generos.json", "r", encoding="utf-8") as g:
                    generos = json.load(g)
                    for g in generos:
                        if g == genero:
                            generos.remove(g)
                            with open("generos.json", "w", encoding="utf-8") as g:
                                json.dump(generos, g, ensure_ascii= False, indent=4)
                                return jsonify({"genero eliminado": genero}), 200
                    return jsonify({"error": "no existe ese genero"}), 400
            else:
                return jsonify({"error": "necesitas permiso de admin para eliminar un genero"}), 403
    
#Endpoint peliculas dirigidas por un director en particular
@app.route("/peliculas/directores/<director>")
def peliculas_director(director):
    with open("peliculas.json", "r", encoding="utf-8") as peliculas:
        peliculas = json.load(peliculas)
        peliculas_director = []
        for pelicula in peliculas:
            if pelicula["director"] == director:
                peliculas_director.append(pelicula)
        if len(peliculas_director) == 0:
            return jsonify({"error": "no hay peliculas dirigidas por ese director"}), 400
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
                            "sinopsis": peliculaNueva["sinopsis"],
                            "visualizaciones": 0}
            peliculas.append(nuevaPelicula)
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, ensure_ascii= False, indent=4)
            return jsonify({"pelicula agregada": nuevaPelicula}), 200


#Endpoint de todas las peliculas del sistema
@app.route("/peliculas")
def peliculas():
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        with open("peliculas.json", "r", encoding="utf-8") as peliculas:
            return jsonify({"peliculas":json.load(peliculas)}), 200
    
@app.route("/peliculas/<int:id>")
def pelicula(id):
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        with open("peliculas.json", "r", encoding="utf-8") as peliculas:
            peliculas = json.load(peliculas)
            for pelicula in peliculas:
                if pelicula["id"] == id:
                    with open("peliculas.json", "w", encoding="utf-8") as p:
                        pelicula["visualizaciones"] += 1
                        json.dump(peliculas, p, ensure_ascii= False, indent=4)
                    return jsonify({"pelicula": pelicula}), 200
            return jsonify({"error": "no existe pelicula con ese id"}), 400


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
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, ensure_ascii= False, indent=4)
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
        with open("comentarios.json", "r", encoding="utf-8") as comentarios:
            comentarios = json.load(comentarios)
            for comentario in comentarios:
                if comentario["ID-pelicula"] == id:
                    if comentario["autor"] != session["usuario"]:
                        return jsonify({"error": "la pelicula tiene comentarios de otros usuarios"}), 401
        with open("peliculas.json", "r", encoding="utf-8") as p:
            peliculas = json.load(p)
            for pelicula in peliculas:
                if pelicula["id"] == id:
                    peliculas.remove(pelicula)
        with open("peliculas.json", "w", encoding="utf-8") as p:
            json.dump(peliculas, p, ensure_ascii= False, indent=4)
            return jsonify({"pelicula eliminada": pelicula}), 200
        
#Endpoint comentarios de pelicula
@app.route("/pelicula/<int:id>/comentarios")
def comentarios_pelicula(id):
    with open("comentarios.json", "r", encoding="utf-8") as comentarios:
        comentarios = json.load(comentarios)
        comentariosPelicula = []
        for comentario in comentarios:
            if comentario["ID-pelicula"] == id:
                comentariosPelicula.append(comentario)
        if len(comentariosPelicula) == 0:
            return jsonify({"error": "esta pelicula no existe o no tiene comentarios"}), 400
        return jsonify({"comentarios de la pelicula": comentariosPelicula}), 200
    
#agregar comentario a pelicula
@app.route("/pelicula/<int:id>/comentarios", methods= ["POST"])
def agregar_comentario(id):
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        comentarioNuevo = request.get_json()
        with open("comentarios.json", "r", encoding="utf-8") as c:
            comentarios = json.load(c)
            mayorId = max(comentarios, key=itemgetter("ID-comentario"))["ID-comentario"] + 1
            nuevoComentario = {"ID-comentario": mayorId, 
                               "ID-pelicula": id, 
                               "autor": session["usuario"], 
                               "comentario": comentarioNuevo["comentario"]}
            comentarios.append(nuevoComentario)
        with open("comentarios.json", "w", encoding="utf-8") as comentariosNuevos:
            json.dump(comentarios, comentariosNuevos, ensure_ascii= False,  indent=4)
            return jsonify({"comentario agregado": nuevoComentario}), 200

#modulo publico
@app.route("/publico")
def publico():
    peliculasPublico = []
    with open("peliculas.json", "r", encoding="utf-8") as p:
        peliculas = json.load(p)
        for pelicula in peliculas:
            peliculasPublico.append(pelicula)
        peliculasPublico = peliculasPublico[-10:]
        peliculasPublico.sort(key = lambda json: json["id"], reverse=True)
        return jsonify({"ultimas 10 peliculas agregadas": peliculasPublico}), 200  
    
#puntuar pelicula
@app.route("/pelicula/<int:id>/puntuacion", methods= ["POST", "DELETE"])
def puntuacion_pelicula(id):
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        if request.method == "POST":
        #recibir json con llave puntuacion y si este usuario ya puntuo esta pelicula modificar la puntuacion
            puntuacion = request.get_json()
            if puntuacion["puntuacion"] > 10 or puntuacion["puntuacion"] < 1:
                return jsonify({"error": "la puntuacion debe ser entre 1 y 10"}), 400
            with open("puntuaciones.json", "r", encoding="utf-8") as p:
                puntuaciones = json.load(p)
                for puntuacionPelicula in puntuaciones:
                    if puntuacionPelicula["ID-pelicula"] == id:
                        if puntuacionPelicula["autor"] == session["usuario"]:
                            puntuacionPelicula["puntuacion"] = puntuacion["puntuacion"]
                            with open("puntuaciones.json", "w", encoding="utf-8") as p:
                                json.dump(puntuaciones, p, ensure_ascii= False, indent=4)
                                return jsonify({"puntuacion modificada": puntuacionPelicula}), 200
            with open("puntuaciones.json", "r", encoding="utf-8") as p:
                puntuaciones = json.load(p)
                nuevaPuntuacion = {"ID-pelicula": id, 
                                   "autor": session["usuario"], 
                                   "puntuacion": puntuacion["puntuacion"]}
                puntuaciones.append(nuevaPuntuacion)
            with open("puntuaciones.json", "w", encoding="utf-8") as p:
                json.dump(puntuaciones, p, ensure_ascii= False, indent=4)
                return jsonify({"puntuacion agregada": nuevaPuntuacion}), 200
        else:
            with open("puntuaciones.json", "r", encoding="utf-8") as p:
                puntuaciones = json.load(p)
                for puntuacionPelicula in puntuaciones:
                    if puntuacionPelicula["ID-pelicula"] == id:
                        if puntuacionPelicula["autor"] == session["usuario"]:
                            puntuaciones.remove(puntuacionPelicula)
                            with open("puntuaciones.json", "w", encoding="utf-8") as p:
                                json.dump(puntuaciones, p, ensure_ascii= False, indent=4)
                                return jsonify({"puntuacion eliminada": puntuacionPelicula}), 200
            return jsonify({"error": "usted no puntuo esta pelicula"}), 400


    
    
#verificar que sos admin
@app.route("/admin")
def admin():
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        return jsonify({"usuario": session["permiso"]}), 200

#asignar nuevo admin
@app.route("/admin", methods= ["POST"])
def asignar_admin():
    if not "usuario" in session:
        return jsonify({"error": "no hay usuario logueado"}), 401
    else:
        if session["permiso"] == "admin":
            nuevoAdmin = request.get_json()
            with open("usuarios.json", "r", encoding="utf-8") as u:
                usuarios = json.load(u)
                for usuario in usuarios:
                    if usuario["nombre"] == nuevoAdmin["usuario"]:
                        usuario["permiso"] = "admin"
                        with open("usuarios.json", "w", encoding="utf-8") as u:
                            json.dump(usuarios, u, ensure_ascii= False, indent=4)
                            return jsonify({"nuevo admin": nuevoAdmin}), 200
                return jsonify({"error": "el usuario no existe"}), 404
        else:
            return jsonify({"error": "solo los admin pueden agregar otros admin"}), 401

                    



if __name__ == "__main__": 
	app.run(debug = True, host="localhost", port=27015)
