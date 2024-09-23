from app.models.account import Account


class AccountRepository:
    """ Requests to account database """

    @staticmethod
    def get_account_by_owner_and_currency(owner_id, currency):
        """ Fetch account by owner id """
        return Account.query.filter_by(owner_id=owner_id, currency=currency).first()

    @staticmethod
    def get_account_by_number(account_number):
        """ Fetch accounts by account number"""
        return Account.query.filter_by(account_number=account_number).first()
