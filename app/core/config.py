import os
from datetime import timedelta


class Config:
    """ Configuration class for the application """
    # MAIN
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')

    # JWT
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY', 'your_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Database Postgresql
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'example'),
        host=os.getenv('DB_HOST', 'database'),
        port=os.getenv('DB_PORT', '5432'),
        db=os.getenv('POSTGRES_DB', 'postgres')
    )
