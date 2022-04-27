# Создание объекта приложения
from flask import Flask

from app.views.node import node
from app.views.users import users
from app.views.warranties import warranties

from app.models import db


def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if app_config is None:
        return None

    app.config.from_object(app_config)

    db.init_app(app)

    app.register_blueprint(node)
    app.register_blueprint(users)
    app.register_blueprint(warranties)

    return app
