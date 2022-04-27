from os import getenv, name

# Для отладки
from dotenv import load_dotenv
load_dotenv()

port = 5434
if name == 'posix':
    port = 5432


class Config:
    SECRET_KEY = getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db}'.format(
        user=getenv('POSTGRES_USER'),
        password=getenv('POSTGRES_PASSWORD'),
        host=getenv('HOST'),
        port=port,
        db=getenv('POSTGRES_DB')
    )
    print(SQLALCHEMY_DATABASE_URI)
    # Не нужно проверять CSRF токен, так как не веб страница
    WTF_CSRF_ENABLED = False
    # Настройка расписания
    # SCHEDULER_API_ENABLED = True


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
