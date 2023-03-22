from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from blog_project.config import Config


db = SQLAlchemy()
login_manager = LoginManager()  # хранит настройки с кот логинишься


def create_app():
    print(__name__)
    app = Flask(__name__)
    login_manager.init_app(app)  # связали проект с сист авторизации

    # во время создания проекта
    from blog_project.main.routes import main
    app.register_blueprint(main)  # регаем блюпринт

    app.config.from_object(Config)  # подключаем конфиг

    return app  # объект класса Flask - приложение
