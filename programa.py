import sys, requests, json

api = "http://localhost:27015/"


def menu_principal():
    print("BIENVENIDO")
    print("1. login")
    print("2. registrarse")
    print("3. ultimas 10 peliculas")
    print("4. salir")


def menu_api():
    print("1. agregar nueva pelicula")
    print("2. editar pelicula")
    print("3. eliminar pelicula")
    print("4. directores de la plataforma")
    print("5. generos de la plataforma")
    print("6. peliculas con mismo director")
    print("7. peliculas con imagen")
    print("8. comentarios de una pelicula")
    print("9. agregar comentario")
    print("10. todas las peliculas registradas")
    print("11. asignar nuevo administrador")
    print("12. buscar pelicula por id")
    print("13. salir")


def error():
    print("opcion invalida")


menuPrincipal = True
menuApi = False
while menuPrincipal:
    menu_principal()
    opcion = int(input())
    if opcion == 1:
        global cookie
        print("ingrese nombre de usuario")
        usuario = input()
        print("ingrese su contraseña")
        contrasena = input()
        datos = {"nombre": usuario, "contraseña": contrasena}
        pet = requests.post(api + "login", json=datos)
        if pet.status_code == 200:
            print("logueado")
            cookie = pet.cookies
            menuApi = True
            menuPrincipal = False
        else:
            print("usuario o contraseña incorrectos")
    elif opcion == 2:
        print("ingrese nombre de usuario")
        usuario = input()
        print("ingrese su contraseña")
        contrasena = input()
        datos = {"nombre": usuario, "contraseña": contrasena}
        pet = requests.post(api + "registro", json=datos)
        if pet.status_code == 200:
            print("registrado")
        else:
            print("usuario o contraseña incorrectos")
    elif opcion == 3:
        pet = requests.get(api + "publico")
        print(pet.text)
    elif opcion == 4:
        sys.exit()
    else:
        error()

while menuApi:
    menu_api()
    opcion = int(input())
    if opcion == 1:
        titulo = input("ingrese el titulo: ")
        petDirectores = requests.get(api + "directores" , cookies=cookie)
        maxid = len(json.loads(petDirectores.text)["directores del sistema"])
        for i, director in enumerate(json.loads(petDirectores.text)["directores del sistema"]):
            print(f"{i}: {director}")
        director = int(input("ingrese el numero del director: "))
        while director >= maxid or director < 0:
            director = int(input("ingrese el numero del director: "))
        directorSeleccionado = json.loads(petDirectores.text)["directores del sistema"][director]
        petGeneros = requests.get(api + "generos", cookies=cookie)
        maxid = len(json.loads(petGeneros.text)["generos del sistema"])
        for i, genero in enumerate(json.loads(petGeneros.text)["generos del sistema"]):
            print(f"{i}: {genero}")
        genero = int(input("ingrese el numero del genero: "))
        while genero >= maxid or genero < 0:
            genero = int(input("ingrese el numero del genero: "))
        generoSeleccionado = json.loads(petGeneros.text)["generos del sistema"][genero]
        imagen = input("ingrese el link a una imagen: ")
        sinopsis = input("ingrese la sinopsis de la pelicula: ")
        datos = {"titulo": titulo, "director": directorSeleccionado, "genero": generoSeleccionado, "imagen": imagen, "sinopsis": sinopsis}
        petSubirPelicula = requests.post(api + "pelicula", json=datos, cookies=cookie)
        print(petSubirPelicula.text)
    elif opcion == 2:
        id = input("ingrese la id de la pelicula que quiere editar: ")
        petPelicula = requests.get(api + "peliculas/" + id, cookies=cookie)
        if petPelicula.status_code == 200:
            titulo = input("ingrese el titulo: ")
            if titulo != "":
                requests.put(api + "pelicula/" + id, json={"titulo": titulo}, cookies=cookie)
            petDirectores = requests.get(api + "directores", cookies=cookie)
            maxid = len(json.loads(petDirectores.text)["directores del sistema"])
            for i, director in enumerate(json.loads(petDirectores.text)["directores del sistema"]):
                print(f"{i}: {director}")
            director = input("ingrese el numero del director: ")
            if director != "":
                while director >= maxid or director < 0:
                    director = input("ingrese el numero del director: ")
                directorSeleccionado = json.loads(petDirectores.text)["directores del sistema"][int(director)]
                requests.put(api + "pelicula/" + id, json={"director": directorSeleccionado}, cookies=cookie)
            petGeneros = requests.get(api + "generos", cookies=cookie)
            maxid = len(json.loads(petGeneros.text)["generos del sistema"])
            for i, genero in enumerate(json.loads(petGeneros.text)["generos del sistema"]):
                print(f"{i}: {genero}")
            genero = input("ingrese el numero del genero: ")
            if genero != "":
                while genero >= maxid or genero < 0:
                    genero = input("ingrese el numero del genero: ")
                generoSeleccionado = json.loads(petGeneros.text)["generos del sistema"][int(genero)]
                requests.put(api + "pelicula/" + id, json={"genero": generoSeleccionado}, cookies=cookie)
            imagen = input("ingrese el link a una imagen: ")
            if imagen != "":
                requests.put(api + "pelicula/" + id, json={"imagen": imagen}, cookies=cookie)
            sinopsis = input("ingrese la sinopsis de la pelicula: ")
            if sinopsis != "":
                requests.put(api + "pelicula/" + id, json={"sinopsis": sinopsis}, cookies=cookie)
        else:
            print("la pelicula no existe")
    elif opcion == 3:
        pelicula = input("ingrese la id de la pelicula que quiere eliminar: ")
        petPelicula = requests.delete(api + "pelicula/" + pelicula, cookies=cookie)
        if petPelicula.status_code == 200:
            print("pelicula eliminada")
        elif petPelicula.status_code == 401:
            print("no puede eliminar una pelicula con comentarios de otros usuarios")
        else:
            print("la pelicula no existe")
    elif opcion == 4:
        print("1: directores de la plataforma")
        print("2: eliminar un director")
        print("3: agregar un director")
        print("4: atras")
        opcion = int(input())
        if opcion == 1:
            petDirectores = requests.get(api + "directores", cookies=cookie)
            print(petDirectores.text)
        elif opcion == 2:
            petDirectores = requests.get(api + "directores" , cookies=cookie)
            maxid = len(json.loads(petDirectores.text)["directores del sistema"])
            for i, director in enumerate(json.loads(petDirectores.text)["directores del sistema"]):
                print(f"{i}: {director}")
            director = int(input("ingrese el numero del director que quiere eliminar: "))
            while director >= maxid or director < 0:
                director = int(input("ingrese el numero del director que quiere eliminar: "))
            directorSeleccionado = json.loads(petDirectores.text)["directores del sistema"][director]
            petEliminarDirector = requests.delete(api + "directores/" + directorSeleccionado, cookies=cookie)
            if petEliminarDirector.status_code == 200:
                print("director eliminado")
            elif petEliminarDirector.status_code == 400:
                print("ese director no existe")
            elif petEliminarDirector.status_code == 403:
                print("solo los admins pueden eliminar directores")
        elif opcion == 3:
            director = input("ingrese el nombre del director a añadir: ")
            petAgregarDirector = requests.post(api + "directores/" + director, cookies=cookie)
            if petAgregarDirector.status_code == 200:
                print("director agregado")
            elif petAgregarDirector.status_code == 400:
                print("ese director ya existe")
            elif petAgregarDirector.status_code == 403:
                print("solo los admins pueden agregar directores")
        elif opcion == 4:
            pass
    elif opcion == 5:
        print("1: generos de la plataforma")
        print("2: eliminar un genero")
        print("3: agregar un genero")
        print("4: atras")
        opcion = int(input())
        if opcion == 1:
            petGeneros = requests.get(api + "generos", cookies=cookie)
            print(petGeneros.text)
        elif opcion == 2:
            petGeneros = requests.get(api + "generos", cookies=cookie)
            maxid = len(json.loads(petGeneros.text)["generos del sistema"])
            for i, genero in enumerate(json.loads(petGeneros.text)["generos del sistema"]):
                print(f"{i}: {genero}")
            genero = int(input("ingrese el numero del genero que quiere eliminar: "))
            while genero >= maxid or genero < 0:
                genero = int(input("ingrese el numero del genero que quiere eliminar: "))
            generoSeleccionado = json.loads(petGeneros.text)["generos del sistema"][genero]
            petEliminarGenero = requests.delete(api + "generos/" + generoSeleccionado, cookies=cookie)
            if petEliminarGenero.status_code == 200:
                print("genero eliminado")
            elif petEliminarGenero.status_code == 400:
                print("ese genero no existe")
            elif petEliminarGenero.status_code == 403:
                print("solo los admins pueden eliminar generos")
        elif opcion == 3:
            genero = input("ingrese el nombre del genero a añadir: ")
            petAgregarGenero = requests.post(api + "generos/" + genero, cookies=cookie)
            if petAgregarGenero.status_code == 200:
                print("genero agregado")
            elif petAgregarGenero.status_code == 400:
                print("ese genero ya existe")
            elif petAgregarGenero.status_code == 403:
                print("solo los admins pueden agregar generos")
        elif opcion == 4:
            pass
    elif opcion == 6:
        director = input("ingrese el director para buscar sus peliculas: ")
        petPeliculas = requests.get(api + "peliculas/directores/" + director, cookies=cookie)
        if petPeliculas.status_code == 200:
            print(petPeliculas.text)
        elif petPeliculas.status_code == 400:
            print("no hay peliculas dirigidas por ese director")
    elif opcion == 7:
        pet = requests.get(api + "peliculas/imagen", cookies=cookie)
        print(pet.text)
    elif opcion == 8:
        pelicula = input("ingrese la id de la pelicula para ver sus comentarios: ")
        pet = requests.get(api + "pelicula/" + pelicula + "/comentarios", cookies=cookie)
        if pet.status_code == 200:
            print(pet.text)
        elif pet.status_code == 400:
            print("esa pelicula no existe o no tiene comentarios")
    elif opcion == 9:
        pelicula = input("ingrese la id de la pelicula que quiere comentar: ")
        comentario = input("ingrese el comentario: ")
        pet = requests.post(api + "pelicula/" + pelicula + "/comentarios", json={"comentario": comentario}, cookies=cookie)
        if pet.status_code == 200:
            print("comentario agregado")
    elif opcion == 10:
        pet = requests.get(api + "peliculas", cookies=cookie)
        
        if len(json.loads(pet.text)["peliculas"]) > 5:
            posComienzo = 0
            posFinal = 5
            while posFinal < len(json.loads(pet.text)["peliculas"]):
                for i, pelicula in enumerate(json.loads(pet.text)["peliculas"][posComienzo:posFinal]):
                    print("\n")
                    print("titulo: " + pelicula["titulo"])
                    print("director: " + pelicula["director"])
                    print("genero: " + pelicula["genero"])
                    print("imagen: " + pelicula["imagen"])
                    print("id: " + str(pelicula["id"]))
                    print("sinopsis: " + pelicula["sinopsis"])
                    print("visualizaciones: " + str(pelicula["visualizaciones"]))
                if posFinal + 5 > len(json.loads(pet.text)["peliculas"]):
                    posComienzo = posFinal
                    posFinal = len(json.loads(pet.text)["peliculas"])
                else:
                    posComienzo = posFinal
                    posFinal += 5
                print("quiere ver mas peliculas? (s/n)")
                opcion = input()
                if opcion == "n":
                    break
        else:
            for i, pelicula in enumerate(json.loads(pet.text)["peliculas"]):
                print("\n")
                print("titulo: " + pelicula["titulo"])
                print("director: " + pelicula["director"])
                print("genero: " + pelicula["genero"])
                print("imagen: " + pelicula["imagen"])
                print("id: " + str(pelicula["id"]))
                print("sinopsis: " + pelicula["sinopsis"])
                print("visualizaciones: " + str(pelicula["visualizaciones"]))
        if len(json.loads(pet.text)["peliculas"]) % 5 != 0:
            for i, pelicula in enumerate(json.loads(pet.text)["peliculas"][posComienzo:]):
                print("\n")
                print("titulo: " + pelicula["titulo"])
                print("director: " + pelicula["director"])
                print("genero: " + pelicula["genero"])
                print("imagen: " + pelicula["imagen"])
                print("id: " + str(pelicula["id"]))
                print("sinopsis: " + pelicula["sinopsis"])
                print("visualizaciones: " + str(pelicula["visualizaciones"]))
    elif opcion == 11:
        usuario = input("ingrese el nombre del usuario al que quiere hacer admin: ")
        #enviar un json con el nombre usuario
        pet = requests.post(api + "/admin", json={"usuario": usuario}, cookies=cookie)
        if pet.status_code == 200:
            print(f"el usuario {usuario} ahora es admin")
        elif pet.status_code == 401:
            print("solo los admins pueden hacer admins")
        elif pet.status_code == 404:
            print("ese usuario no existe")
    elif opcion == 12:
        pelicula = input("ingrese la id de la pelicula que quiere buscar: ")
        pet = requests.get(api + "peliculas/" + pelicula, cookies=cookie)
        if pet.status_code == 200:
            print(pet.text)
            print("1: agregar o modificar puntuacion")
            print("2: eliminar puntuacion")
            print("3: volver")
            opcion = int(input())
            if opcion == 1:
                puntuacion = int(input("ingrese la puntuacion: "))
                pet = requests.post(api + "pelicula/" + pelicula + "/puntuacion", json={"puntuacion": puntuacion}, cookies=cookie)
                if pet.status_code == 200:
                    print(pet.text)
                elif pet.status_code == 400:
                    print("la puntuacion debe estar entre 1 y 10")
                
            elif opcion == 2:
                pet = requests.delete(api + "pelicula/" + pelicula + "/puntuacion", cookies=cookie)
                if pet.status_code == 200:
                    print(pet.text)
                elif pet.status_code == 400:
                    print("usted no puntuo esa pelicula")
            elif opcion == 3:
                pass
        elif pet.status_code == 400:
            print("esa pelicula no existe")
    elif opcion == 13:
        break















