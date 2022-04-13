class Config:
    # todo имопрт токена из sh файлика
    SECRET_KEY = 'P0t3()Au6(w0n7G)'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # todo брать данные аутентификации бд из sh файлика
    SQLALCHEMY_DATABASE_URI = 'postgres://ddbuser:ul9(tOjl&3H6%0q#@{}:5432/ddb'.format('23.111.204.215')
    # SQLALCHEMY_DATABASE_URI = 'postgres://dora_admin:neOXvhpbb44u@{}:8917/dora_database'.format('23.111.204.215')
    # Не нужно проверять CSRF токен, так как не веб страница
    WTF_CSRF_ENABLED = False
    # Настройки Flask-Mail
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'no-reply@dora.team'
    MAIL_PASSWORD = 'vjbpflsmadiitzoi'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    # Настройка расписания
    SCHEDULER_API_ENABLED = True


class ProdConfig(Config):
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    DEBUG = True
    TESTING = False
