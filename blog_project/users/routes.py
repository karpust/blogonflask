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
    if current_user.is_authenticated:  # current_user - залогиненый или анонимус
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():  # если 'POST'-запрос и все поля валидны:
        user = User.query.filter_by(email=form.email.data).first()  # выбрали из бд юзера по почте

        # если такой юзер есть и его пароль совпадает с введенным в форму (хеши), перенаправим на главную:
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.to_remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # если 'POST' и поля валидны:
        if form.picture.data:  # если в форме выбрали фото
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file  # добавляем юзеру фотку в бд (image_file - поле таблицы бд)
        current_user.username = form.username.data  # изменяем на то что ввели в форму
        current_user.email = form.email.data
        db.session.commit()  # изменили в юзера в бд
        flash('Ваш аккаунт был успешно обновлен!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.username.data = current_user.username  # в форме отображ старые данные, не пустая
        form.email.data = current_user.email
    page = request.args.get('page', 1, type=int)  # пагинация: список постов с 1-ой стр   ??? откуда там брать арги
    user = User.query.filter_by(username=form.username.data).first_or_404()  # ?получаем юзера из бд
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # ???
    return render_template('account.html', title='Аккаунт', image_file=image_file, form=form, posts=posts,
                           user=user)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
