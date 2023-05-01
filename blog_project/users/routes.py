from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog_project import db, bcrypt
from blog_project.models import User, Post
from blog_project.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    RequestResetForm, ResetPasswordForm
from blog_project.users.utils import save_picture, send_reset_email


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

        # если такой юзер есть и его пароль совпадает с введенным в форму (хеши):
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.to_remember.data)

            # запоминаем стр на кот юзер был до авторизации:
            next_page = request.args.get('next')
            # и перенапрявляем на нее; если юзер сразу пошел логиниться, перенаправляем на все посты:
            return redirect(next_page) if next_page else redirect(url_for('posts.allposts'))
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
        db.session.commit()  # изменили юзера в бд
        flash('Ваш аккаунт был успешно обновлен!', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.username.data = current_user.username  # в форме отображ старые данные, не пустая
        form.email.data = current_user.email
        form.picture.data = current_user.image_file
    # page = request.args.get('page', 1, type=int)  # пагинация: список постов с 1-ой стр   ??? откуда там брать арги
    # posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    # user = User.query.filter_by(username=form.username.data).first_or_404()
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # +-
    return render_template('account.html', title='Аккаунт', form=form, image_file=image_file)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.allposts'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На почту отправлено письмо для сброса пароля.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Сброс пароля', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('posts.allposts'))
    user = User.verify_reset_token(token)
    if not user:
        flash('Недействительный или просроченный токен')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был успешно обновлен!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Сброс пароля', form=form)
