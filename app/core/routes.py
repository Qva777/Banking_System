from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'Hello, this is the Flask home page'
