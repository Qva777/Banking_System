from flask import jsonify


def handle_http_exception(error):
    """ Error handler function for all blueprints """
    response = {
        "error": error.name,
        "message": error.description,
        "code": error.code
    }
    return jsonify(response), error.code
