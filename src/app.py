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
@app.route('/users', methods=['GET'])
def get_users():
    all_users= User.query.all()
    if all_users == []: #si mi array esta vacio entonces return envia el msj no exiten usarios
        return jsonify({"msj":"no existen usarios"}), 404 #si entra en el if la duncion termina ahi.
    
    result= list(map(lambda item:item.serialize(),all_users)) # linea de codigo que me perite listar todos los usuarios

    response_body = {
        "msg": "Estos son tus usuarios", 
        "results": result #muestra tus usuarios todos listados
    }
    return jsonify(response_body), 200

#ENDPOINT PERSONAJES
@app.route('/characters', methods=['GET'])
def get_characters():
    all_characters= Characters.query.all()
    result= list(map(lambda item:item.serialize(),all_characters))

    response_body = {
        "msg": "Estos son tus personajes",
        "results": result
    }
    return jsonify(response_body), 200

#ENDPOINT PLANETAS
@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets= Planets.query.all()
    result= list(map(lambda item:item.serialize(),all_planets))

    response_body = {
        "msg": "Estos son tus planetas",
        "results": result
    }
    return jsonify(response_body), 200

#ENDPOINT FAVORITOS
@app.route('/user/<int:id>/favorites', methods=['GET']) #cada vez que tengo una ruta dinamico id(dinamico) tenfo que pasarlo como parametro
def get_favorites(id):
    print(id)
    user_resul = Favorites.query.filter_by(user_id=id).all()# filter_by(propiedad a consultar=memoria donde se guarda el dato) 
    print(user_resul)
    result= list(map(lambda item:item.serialize(),user_resul)) # linea de codigo que me perite listar todos los favoritos
    print(result)
    response_body = {
        "msg": "Estos son tus favoritos", 
        "results": result #muestra tus favoritos todos listados
    }
    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
