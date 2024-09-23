from app import db
from app.core.behaviors import Timestampable, SoftDeletionModel
from werkzeug.security import check_password_hash


class User(SoftDeletionModel, Timestampable):
    """ User model """
    __tablename__ = 'users'

    name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    accounts = db.relationship('Account', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __str__(self):
        return f'User {self.name}'

    def verify_password(self, password):
        """ Verify the password hash """
        return check_password_hash(self.password, password)
