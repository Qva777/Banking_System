import enum
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID

from app import db
from app.core.behaviors import Timestampable, SoftDeletionModel


class CurrencyChoice(enum.Enum):
    """ Choice for currencies """
    USD = "USD"
    EUR = "EUR"


class Account(SoftDeletionModel, Timestampable):
    """ Account Model """

    __tablename__ = 'accounts'
    __table_args__ = (db.UniqueConstraint('currency', 'owner_id', name='uq_currency_owner'),)

    account_number = db.Column(db.String(16), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False)
    currency = db.Column(Enum(CurrencyChoice), nullable=False)
    owner_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    def __str__(self):
        return f'Account {self.account_number} - Owner: {self.owner.name} - Currency: {self.currency.value}'
