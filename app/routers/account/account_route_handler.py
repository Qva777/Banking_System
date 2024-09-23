import random
from flask import abort, jsonify
from app.models.account import Account, CurrencyChoice
from app.repositories.account_repository import AccountRepository
from app.repositories.common import CommonRepository
from app.repositories.user_repository import UserRepository
from app.utils.validators import validate_balance


class AccountHandlers:

    @staticmethod
    def create_account(name, initial_balance, currency):
        """ Handle the logic to create an account """

        validate_balance(initial_balance)
        user = UserRepository.get_user_by_name(name)
        abort(404, description="User not found") if not user else None

        if currency not in [choice.value for choice in CurrencyChoice]:
            abort(400, description="Invalid currency, available currencies: 'EUR' and 'USD' ")
        existing_account = AccountRepository.get_account_by_owner_and_currency(user.id, CurrencyChoice[currency])
        if existing_account:
            abort(400, description="Account with this currency already exists for the user")

        # Generate a 16-digit random account number
        account_number = str(random.randint(10 ** 15, 10 ** 16 - 1))

        new_account = Account(
            account_number=account_number,
            balance=initial_balance,
            currency=CurrencyChoice[currency],
            owner_id=user.id
        )
        CommonRepository.save_instance(new_account)
        return jsonify({
            "message": "Account created successfully",
            "account": {
                "id": new_account.id,
                "account_number": new_account.account_number,
                "balance": new_account.balance,
                "currency": new_account.currency.value,
                "owner_id": new_account.owner_id,
                "created_at": new_account.created_at,
                "updated_at": new_account.updated_at,
            }
        })

    @staticmethod
    def deposit(account_number, amount):
        """ Handle the logic to make a deposit """
        account = AccountRepository.get_account_by_number(account_number)
        abort(404, description="Account not found") if not account else None

        account.balance += amount
        CommonRepository.commit_changes()
        return jsonify({
            "message": "Deposit successful",
            "account_number": account.account_number,
            "currency": account.currency.value,
            "balance": account.balance
        })

    @staticmethod
    def withdraw(account_number, amount):
        """ Handle the logic to make a withdrawal """
        account = AccountRepository.get_account_by_number(account_number)
        abort(404, description="Account not found") if not account else None

        if account.balance < amount:
            abort(400, description="Insufficient balance for the withdrawal")

        account.balance -= amount
        CommonRepository.commit_changes()
        return jsonify({
            "message": "Withdrawal successful",
            "account_number": account.account_number,
            "currency": account.currency.value,
            "balance": account.balance
        })

    @staticmethod
    def transfer(from_account_number, to_account_number, amount):
        """ Handle the logic to make a transfer """
        from_account = AccountRepository.get_account_by_number(from_account_number)
        to_account = AccountRepository.get_account_by_number(to_account_number)

        abort(404, description="From account not found") if not from_account else None
        abort(404, description="To account not found") if not to_account else None

        if from_account.balance < amount:
            abort(400, description="Insufficient balance for the transfer")

        from_account.balance -= amount
        to_account.balance += amount
        CommonRepository.commit_changes()
        return jsonify({
            "message": "Transfer successful",
            "from_account": {
                "account_number": from_account.account_number,
                "balance": from_account.balance
            },
            "to_account": {
                "account_number": to_account.account_number,
                "balance": to_account.balance
            }
        })
