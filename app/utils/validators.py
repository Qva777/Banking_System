from flask import abort


def validate_balance(balance):
    """ Validates the balance ensuring it's positive, non-zero, and less than or equal to 100,000 """
    if balance <= 0:
        abort(400, description="Balance must be greater than 0")
    if balance > 100000:
        abort(400, description="money by one request cannot be more than 100,000")
