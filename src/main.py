"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from .utils import APIException, generate_sitemap
from .admin import setup_admin
from .db import db
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import date, time, datetime, timezone
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Change this!
jwt = JWTManager(app)

# Setup de Bcrypt
bcrypt = Bcrypt(app)


MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#####  Importar Modelos  ####
from src.modelos import Blocked, User, Planets, People, Vehicles, Favorite_People, Favorite_Planets, Favorite_Vehicles 

##### Importar las Rutas ####
from src.rutas import signup, user_login, user_logout, user_profile, get_user_by_id, delete_user_by_id, get_users, hello_protected, allUsers
from src.rutas import get_people, get_people_by_id, create_new_person, put_people_by_id, busqueda_people, delete_character_by_id
from src.rutas import get_planets, get_planet_by_id, create_new_planet, delete_planet_by_id
from src.rutas import get_vehicles, get_vehicle_by_id, create_new_vehicle, delete_vehicle_by_id



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usergettest', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
