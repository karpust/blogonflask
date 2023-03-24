from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog_project import db, bcrypt
from blog_project.models import User, Post
from blog_project.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    RequestResetForm, ResetPasswordForm
from blog_project.users.utils import save_picture

users = Blueprint('users', __name__)  # name, import_name


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись создана!'
              'Теперь вы можете войти в систему.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


# в шаблоне header.html используется динамическая ссылка
# {{ url_for('users.register') }}
# где: users - блюпринт, register - его маршрут /register

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # выбрали из бд юзера по почте

        # если такой юзер есть и его пароль совпадает с введенным в форму (хеши), перенаправим на главную:
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.to_remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)
