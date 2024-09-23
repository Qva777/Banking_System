from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import HTTPException

from app.schemas.user import UserSchema
from app.routers.error_handlers import handle_http_exception
from app.routers.user.user_route_handler import UserHandlers, UserAuthHandlers

api_user = Blueprint('api_user', __name__)

# Register the error handler
api_user.register_error_handler(HTTPException, handle_http_exception)


@api_user.route('/login_jwt', methods=['POST'])
def login():
    """ Endpoint to log in a user using JWT """
    data = request.get_json()
    tokens, error = UserAuthHandlers.login(data)
    abort(400, description=error) if error == "Missing required fields" else None
    abort(401, description=error) if error == "Invalid credentials" else None
    return jsonify(tokens), 200


@api_user.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """ Endpoint to refresh the access token """
    tokens = UserAuthHandlers.refresh_token()
    return jsonify(tokens), 200


@api_user.route('/users', methods=['POST'])
def create_user():
    """ API endpoint to create a new user """
    data = request.get_json()
    new_user, error = UserHandlers.create_user(data)
    abort(400, description=error) if error else None

    user_schema = UserSchema()
    return jsonify({
        "message": "User created successfully",
        "user": user_schema.dump(new_user)
    }), 201


@api_user.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """ Endpoint to retrieve all users(alive) """
    users_data = UserHandlers.get_users()
    return jsonify(users_data), 200


@api_user.route('/users/<uuid:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    """ Endpoint to retrieve a user by their ID """
    user_data, error = UserHandlers.get_user_by_id(id)
    abort(404, description=error) if error else None
    return jsonify({"user": user_data}), 200


@api_user.route('/users/<uuid:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """ Endpoint to update a user by their ID """
    data = request.get_json()
    user_data, error = UserHandlers.update_user_by_id(id, data)

    if error:
        if isinstance(error, dict):
            abort(400, description=error)
        else:
            abort(404, description=error)

    return jsonify({"message": "User updated successfully", "user": user_data}), 200


@api_user.route('/users/<uuid:id>', methods=['DELETE'])
@jwt_required()
def soft_delete_user(id):
    """ Endpoint soft delete user by ID """
    response, error = UserHandlers.soft_deletion_user_by_id(id)
    abort(404, description=error) if error else None
    return response, 200


@api_user.route('/users/<uuid:id>/hard_delete', methods=['DELETE'])
@jwt_required()
def hard_delete_user(id):
    """ Endpoint hard delete user by ID """
    response, error = UserHandlers.hard_deletion_user_by_id(id)
    abort(404, description=error) if error else None
    return response, 200


@api_user.route('/users/<uuid:id>/recover', methods=['POST'])
@jwt_required()
def recover_user(id):
    """ Endpoint recover deleted user by ID """
    response, error = UserHandlers.recover_deleted_user_by_id(id)
    abort(404, description=error) if error else None
    return response, 200


@api_user.route('/deleted_users', methods=['GET'])
@jwt_required()
def get_deleted_users():
    """ Endpoint deleted users """
    response = UserHandlers.get_deleted_users()
    return response, 200
