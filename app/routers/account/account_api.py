from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import HTTPException

from app.utils.validators import validate_balance
from app.routers.account.account_route_handler import AccountHandlers
from app.routers.error_handlers import handle_http_exception

api_account = Blueprint('api_account', __name__)

# Register the error handler
api_account.register_error_handler(HTTPException, handle_http_exception)


@api_account.route('/create_account', methods=['POST'])
@jwt_required()
def create_account():
    """ Endpoint to create an account """
    data = request.get_json()
    name = data.get('name')
    initial_balance = data.get('initial_balance')
    currency = data.get('currency')

    if not name or initial_balance is None or not currency:
        abort(400, description="Missing required fields")

    response = AccountHandlers.create_account(name, initial_balance, currency)
    return response, 201


@api_account.route('/deposit', methods=['POST'])
@jwt_required()
def deposit():
    """ Endpoint to make a deposit """

    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')

    if not account_number or amount is None:
        abort(400, description="Missing required fields")

    validate_balance(amount)
    response = AccountHandlers.deposit(account_number, amount)
    return response, 200


@api_account.route('/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    """ Endpoint to make a withdrawal """

    data = request.get_json()
    account_number = data.get('account_number')
    amount = data.get('amount')

    if not account_number or amount is None:
        abort(400, description="Missing required fields (account_number or amount)")

    validate_balance(amount)
    response = AccountHandlers.withdraw(account_number, amount)
    return response, 200


@api_account.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    """ Endpoint to make a transfer from one to another account """
    data = request.get_json()
    from_account_number = data.get('from_account_number')
    to_account_number = data.get('to_account_number')
    amount = data.get('amount')

    if not from_account_number or not to_account_number or amount is None:
        abort(400, description="Missing required fields")

    validate_balance(amount)
    response = AccountHandlers.transfer(from_account_number, to_account_number, amount)
    return response, 200
