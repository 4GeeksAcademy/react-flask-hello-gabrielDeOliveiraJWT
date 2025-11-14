from flask import request, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.models import db, User, Character, Sith, Starship
from api.utils import generate_sitemap, APIException

api = Blueprint("api", __name__)
CORS(api)

@api.route("/hello", methods=["POST", "GET"])
def handle_hello():
    response_body = {"message": "Hello! I'm a message that came from the backend"}
    return jsonify(response_body), 200

@api.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "email and password are required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "email already exists"}), 400
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        email=data["email"],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "user created"}), 201

@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "email and password are required"}), 400
    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"msg": "bad email or password"}), 401
    if not check_password_hash(user.password, data["password"]):
        return jsonify({"msg": "bad email or password"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200

@api.route("/private", methods=["GET"])
@jwt_required()
def private():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "user not found"}), 404
    return jsonify({"msg": "ok", "user": user.serialize()}), 200

@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"msg": "email and password are required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "email already exists"}), 400
    hashed_password = generate_password_hash(data["password"])
    new_user = User(
        email=data["email"],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

@api.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"msg": "User deleted"}), 200

@api.route("/characters", methods=["GET"])
def get_characters():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

@api.route("/characters/<int:character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@api.route("/characters", methods=["POST"])
def create_character():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("img"):
        return jsonify({"msg": "name and img are required"}), 400
    new_character = Character(
        name=data["name"],
        img=data["img"]
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

@api.route("/characters/<int:character_id>", methods=["DELETE"])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msg": "Character not found"}), 404
    db.session.delete(character)
    db.session.commit()
    return jsonify({"msg": "Character deleted"}), 200

@api.route("/siths", methods=["GET"])
def get_siths():
    siths = Sith.query.all()
    return jsonify([sith.serialize() for sith in siths]), 200

@api.route("/siths/<int:sith_id>", methods=["GET"])
def get_sith(sith_id):
    sith = Sith.query.get(sith_id)
    if not sith:
        return jsonify({"msg": "Sith not found"}), 404
    return jsonify(sith.serialize()), 200

@api.route("/siths", methods=["POST"])
def create_sith():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("img"):
        return jsonify({"msg": "name and img are required"}), 400
    new_sith = Sith(
        name=data["name"],
        img=data["img"]
    )
    db.session.add(new_sith)
    db.session.commit()
    return jsonify(new_sith.serialize()), 201

@api.route("/siths/<int:sith_id>", methods=["DELETE"])
def delete_sith(sith_id):
    sith = Sith.query.get(sith_id)
    if not sith:
        return jsonify({"msg": "Sith not found"}), 404
    db.session.delete(sith)
    db.session.commit()
    return jsonify({"msg": "Sith deleted"}), 200

@api.route("/starships", methods=["GET"])
def get_starships():
    starships = Starship.query.all()
    return jsonify([starship.serialize() for starship in starships]), 200

@api.route("/starships/<int:starship_id>", methods=["GET"])
def get_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"msg": "Starship not found"}), 404
    return jsonify(starship.serialize()), 200

@api.route("/starships", methods=["POST"])
def create_starship():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("img"):
        return jsonify({"msg": "name and img are required"}), 400
    new_starship = Starship(
        name=data["name"],
        img=data["img"]
    )
    db.session.add(new_starship)
    db.session.commit()
    return jsonify(new_starship.serialize()), 201

@api.route("/starships/<int:starship_id>", methods=["DELETE"])
def delete_starship(starship_id):
    starship = Starship.query.get(starship_id)
    if not starship:
        return jsonify({"msg": "Starship not found"}), 404
    db.session.delete(starship)
    db.session.commit()
    return jsonify({"msg": "Starship deleted"}), 200