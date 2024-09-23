import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.core.config import Config
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

migrate = Migrate()
db = SQLAlchemy()


def create_app():
    """ Initialize the Flask app """

    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .models.user import User
        from .models.account import Account
        db.create_all()

    from app.core.routes import main
    from app.routers.user.user_api import api_user
    from app.routers.account.account_api import api_account

    app.register_blueprint(main)
    app.register_blueprint(api_user, url_prefix='/api')
    app.register_blueprint(api_account, url_prefix='/api')
    return app
