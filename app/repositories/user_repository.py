from app import db
from app.models.user import User


class UserRepository:
    """ Requests to user database """

    @staticmethod
    def get_user_by_name(name):
        """ Fetch a user by name from the database """
        return User.query.filter_by(name=name).first()

    @staticmethod
    def get_user_by_id(user_id):
        """ Fetch a user by their ID """
        return User.query.get(user_id)

    @staticmethod
    def get_whole_user_details(user_id):
        """ Fetch a user with details about the bank account """
        return (
            User.query
            .options(
                db.joinedload(User.accounts).load_only('account_number', 'balance'),
                db.load_only('id', 'name')
            )
            .filter_by(id=user_id)
            .first()
        )

    @staticmethod
    def get_all_users():
        """ Fetch all users(alive) """
        return User.query_alive().all()
