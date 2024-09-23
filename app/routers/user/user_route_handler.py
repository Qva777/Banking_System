from flask import abort, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError

from app.repositories.common import CommonRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserSchema
from app.models.user import User


class UserAuthHandlers:
    @staticmethod
    def login(data):
        """ Handle user login logic """
        name = data.get('name')
        password = data.get('password')

        if not name or not password:
            return None, "Missing required fields(name or password)"

        # Fetch user from the repository
        user = UserRepository.get_user_by_name(name)

        # Verify credentials
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, None

        return None, "Invalid credentials"

    @staticmethod
    def refresh_token():
        """ Handle token refresh logic """
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return {"access_token": new_access_token}


class UserHandlers:

    @staticmethod
    def create_user(data):
        """ Handles the creation of a new user """
        user_schema = UserSchema()

        try:
            user_data = user_schema.load(data)
        except ValidationError as err:
            return None, err.messages

        if UserRepository.get_user_by_name(user_data['name']):
            return None, "User with this name already exists"

        hashed_password = generate_password_hash(user_data['password'])
        new_user = User(name=user_data['name'], password=hashed_password)
        CommonRepository.save_instance(new_user)
        return new_user, None

    @staticmethod
    def get_users():
        """ Handle the logic to get all users(alive) """
        users = UserRepository.get_all_users()
        result = []

        for user in users:
            user_data = {
                "id": user.id,
                "name": user.name,
                "user_accounts": [
                    {
                        "account_number": account.account_number,
                        "currency": account.currency.value,
                        "balance": account.balance
                    }
                    for account in user.accounts
                ]
            }
            result.append(user_data)

        return result

    @staticmethod
    def get_deleted_users():
        """ Handle the logic to get all users(deleted) """
        users = CommonRepository.get_deleted_instance(User)
        return jsonify([f"{str(user)} {str(user.id)}" for user in users])

    @staticmethod
    def get_user_by_id(user_id):
        """ Handle the logic to get a user by ID """
        user = UserRepository.get_user_by_id(user_id)

        if not user:
            return None, "User not found"

        user_data = {
            "id": user.id,
            "name": user.name,
            "user_accounts": [
                {
                    "currency": account.currency.value,
                    "account_number": account.account_number,
                    "balance": account.balance
                }
                for account in user.accounts
            ]
        }
        return user_data, None

    @staticmethod
    def update_user_by_id(user_id, data):
        """ Handle logic for updating a user by their ID """
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None, "User not found"

        user_schema = UserSchema(partial=True)
        try:
            user_data = user_schema.load(data)
        except ValidationError as err:
            return None, err.messages

        if 'name' in user_data:
            user.name = user_data['name']
        if 'password' in user_data:
            user.password = generate_password_hash(user_data['password'])

        CommonRepository.commit_changes()
        return user_schema.dump(user), None

    @staticmethod
    def soft_deletion_user_by_id(user_id):
        """ Handle logic for soft deleting a user by their ID """
        user = UserRepository.get_user_by_id(user_id)
        abort(404, description="User not found") if not user else None
        CommonRepository.delete_instance(User, user)
        return {"message": "User soft deleted"}, None

    @staticmethod
    def hard_deletion_user_by_id(user_id):
        """ Handle logic for hard deleting a user by their ID """
        user = UserRepository.get_user_by_id(user_id)
        abort(404, description="User not found") if not user else None
        CommonRepository.hard_delete_instance(User, user)
        return {"message": "User hard deleted"}, None

    @staticmethod
    def recover_deleted_user_by_id(user_id):
        """ Handle logic recover deleted a user by their ID """
        user = UserRepository.get_user_by_id(user_id)
        abort(404, description="User not found") if not user else None
        CommonRepository.recover_instance(user)
        return {"message": "User recovered"}, None
