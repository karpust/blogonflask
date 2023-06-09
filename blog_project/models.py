from datetime import datetime
from blog_project import db, login_manager
from flask_login import UserMixin
from authlib.jose import JsonWebSignature
from flask import current_app
import json

jws = JsonWebSignature()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# определяем модель User:
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,  # не Null
                           default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # связь с табл Post,тк uselist по дефолту, то постов несколько,
    # backref='author' - классу Post объявили новое свойство author
    # lazy=True is SELECT - связанные записи таблиц(юзеры, посты) загруж параллельно

    def get_reset_token(self):  # used authlib instead of itsdangerous
        key = current_app.config['SECRET_KEY']
        payload = json.dumps({'user_id': self.id})
        s = jws.serialize_compact(protected={'alg': 'HS256'}, payload=payload, key=key)
        return s

    @staticmethod
    def verify_reset_token(token):
        key = current_app.config['SECRET_KEY']
        s = jws.deserialize_compact(token, key)['payload']  # b'{"user_id": 4}'
        try:
            user_id = json.loads(s)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"Пользователь('{self.username}',' {self.email}', ' {self.image_file}')"


# определяем модель Post:
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"
