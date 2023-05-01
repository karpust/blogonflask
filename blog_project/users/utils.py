import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog_project import mail


def save_picture(form_picture):
    random_hex = token_hex(8)  # 8 байтов каждый в 2 шестнадцатир цифры: '1923b6a471070650'
    _, f_ext = os.path.splitext(form_picture.filename)  # ('2', '.jpg')
    picture_fn = random_hex + f_ext  # '1923b6a471070650.jpg'
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    # 'C:\\Users\\k\\PycharmProjects\\blogonflask\\blog_project\\static/profile_pics\\1923b6a471070650.jpg'
    output_size = (150, 150)
    i = Image.open(form_picture)  # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=283x178 at 0x1EB776B6920>
    i.thumbnail(output_size)  # <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=150x94 at 0x2015F7806D0>
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Запрос на сброс пароля', sender='karpu5t@yandex.ru', recipients=[user.email])
    msg.body = f'''Чтобы сбросить пароль перейдите по ссылке: 
    {url_for('users.reset_token', token=token, _external=True)}.
    Проигнорируйте это письмо, если вы не отправляли запрос на сброс пароля'''
    mail.send(msg)
