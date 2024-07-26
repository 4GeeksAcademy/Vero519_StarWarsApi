"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Characters
from models import db, Planets
from models import db, User
from models import db, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#ENDPOINT USUARIOS
#GET Usuarios
@app.route('/users', methods=['GET'])
def get_users():
    all_users= User.query.all()
    if all_users == []: #si mi array esta vacio entonces return envia el msj no exiten usarios
        return jsonify({"msj":"No existen usarios"}), 404 #si entra en el if la funcion termina ahi.
    
    result= list(map(lambda item:item.serialize(),all_users)) # linea de codigo que me perite listar todos los usuarios

    response_body = {
        "msg": "Estos son tus usuarios", 
        "results": result #muestra tus usuarios todos listados
    }
    return jsonify(response_body), 200

#GET para un usuario

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    # print(id)
    especific_user= User.query.filter_by(id=id).first()
    if especific_user is None:
        return jsonify({"msj":"El usuario no existe"}), 404
    # print(especific_user)
    query_result= especific_user.serialize()
    print(query_result)
    return jsonify(query_result), 200

#POST User (Crear un usuario)

@app.route('/users', methods=['POST'])
def add_new_user():
    request_body= request.get_json()
    # print(request_body)
    especific_user= User.query.filter_by(email=request_body['email']).first() #me permite filtrar si el email existe
    if especific_user:
        return jsonify({"msj":"El usuario ya existe"}), 404 #en el caso que exista me avisa y da el error 404
    
    new_user = User(
        name = request_body['name'],# informacion que quiero de mi usuario y que tengo contenida en mi request_body
        email = request_body['email'],
        pasword = request_body['password']
    )
    # print(new_user)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msj":"El usuario fue creado"}), 201


#ENDPOINT PERSONAJES
#GET Personajes
@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters= Characters.query.all()
    result= list(map(lambda item:item.serialize(),all_characters))

    response_body = {
        "msg": "Estos son tus personajes",
        "results": result
    }
    return jsonify(response_body), 200

#GET Personaje
@app.route('/characters/<int:id>', methods=['GET'])
def get_character(id):
    # print(id)
    especific_character= Characters.query.filter_by(id=id).first()
    # print(especific_character)
    query_result= especific_character.serialize()
    # print(query_result)
    return jsonify(query_result), 200

#ENDPOINT PLANETAS
#GET Planetas
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets= Planets.query.all()
    result= list(map(lambda item:item.serialize(),all_planets))
    response_body = {
        "msg": "Estos son tus planetas",
        "results": result
    }
    return jsonify(response_body), 200

#GET Planeta
@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
    especific_planet= Planets.query.filter_by(id=id).first()
    # print(especific_planet)
    query_result= especific_planet.serialize()
    return jsonify(query_result), 200


#ENDPOINT FAVORITOS
#GET Favoritos
@app.route('/user/<int:id>/favorites', methods=['GET']) #cada vez que tengo una ruta dinamica (ej.id) tengo que pasarlo como parametro
def get_favorites(id):
    print(id) #imprime mis id
    user_resul = Favorites.query.filter_by(user_id=id).all()# filter_by(propiedad a consultar=memoria donde se guarda el dato) 
    print(user_resul)
    result= list(map(lambda item:item.serialize(),user_resul)) # linea de codigo que me perite listar todos los favoritos
    print(result)
    response_body = {
        "msg": "Estos son tus favoritos", 
        "results": result #muestra tus favoritos todos listados
    }
    return jsonify(response_body), 200

#POST Personaje_Favorito (agregar un Personaje a Favoritos)
@app.route('/favorites/character/<int:id>', methods=['POST'])
def add_new_character_fav(id):
    request_body= request.get_json()
    especific_user= User.query.filter_by(id=request_body['user_id']).first() #me permite filtrar si el usuario existe
    if especific_user is None:
        return jsonify({"msj":"El usuario no existe"}), 404 #en el caso que exista me avisa y da el error 404
    
    especific_character= Characters.query.filter_by(id=id).first() 
    if especific_character is None:
        return jsonify({"msj":"El personaje no existe"}), 404 #en el caso que exista me avisa y da el error 404

    new_favorite = Favorites(
        user_id  = request_body['user_id'],# informacion que quiero de mi usuario y que tengo contenida en mi request_body
        characters_id = id, #es solo id porque ya lo obtengo en mi ruta
    )

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msj":"Tu favorito fue creado"}), 201

   #POST Planeta Favorito
@app.route('/favorites/planets/<int:id>', methods=['POST'])
def add_new_planet_fav(id):
    request_body= request.get_json()
    especific_user= User.query.filter_by(id=request_body['user_id']).first() #me permite filtrar si el usuario existe
    if especific_user is None:
        return jsonify({"msj":"El usuario no existe"}), 404 #en el caso que exista me avisa y da el error 404
    
    especific_planet= Planets.query.filter_by(id=id).first() 
    if especific_planet is None:
        return jsonify({"msj":"El planeta no existe"}), 404 #en el caso que exista me avisa y da el error 404

    new_favorite = Favorites(
        user_id  = request_body['user_id'],# informacion que quiero de mi usuario y que tengo contenida en mi request_body
        planets_id = id, #es solo id porque ya lo obtengo en mi ruta y planet_id es de mi models.py
    )

    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msj":"Tu favorito fue creado"}), 201

#ENDPOINT DELETE
@app.route('/favorites/<int:id>', methods=['DELETE'])
def delete_fav(id):
    especific_fav= Favorites.query.filter_by(id=id).first() #me permite filtrar si el usuario existe
    if especific_fav is None:
        return jsonify({"msg":"No existe el favorito"}), 404#result es mi lista de favoritos para ese id
    

    db.session.delete(especific_fav)
    db.session.commit()    
    return jsonify({"msj":"Se ha elimidado tu favorito"}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
