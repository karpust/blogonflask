from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from blog_project.config import Config
from flask_bcrypt import Bcrypt

# дока https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/
db = SQLAlchemy()
login_manager = LoginManager()  # хранит настройки с кот логинишься
bcrypt = Bcrypt()


def create_app():
    print(__name__)
    app = Flask(__name__)
    login_manager.init_app(app)  # связали проект с сист авторизации
    bcrypt.init_app(app)

    # во время создания проекта
    from blog_project.main.routes import main
    from blog_project.users.routes import users

    app.register_blueprint(main)  # регаем блюпринты
    app.register_blueprint(users)

    app.config.from_object(Config)  # подключаем конфиг

    db.init_app(app)  # связали приложение с алхимией

    # создаем таблицы в бд по ранее определенным моделям:
    with app.app_context():
        db.create_all()

    return app  # объект класса Flask - приложение
