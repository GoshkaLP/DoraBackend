from os import getenv

# Для отладки
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        host=getenv('HOST'),
        port=5434,
        db=getenv('POSTGRES_DB')
    )
    # Не нужно проверять CSRF токен, так как не веб страница
    WTF_CSRF_ENABLED = False
    # Настройки Flask-Mail
    MAIL_SERVER = getenv('MAIL_SERVER')
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    # Настройка расписания
    # SCHEDULER_API_ENABLED = True


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
