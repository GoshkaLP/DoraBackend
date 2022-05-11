from app.controllers.responses_controller import resp_ok, resp_wrong_email_format, \
    resp_account_exists, resp_form_not_valid, resp_account_not_exists, resp_wrong_password, resp_old_password

from app.models import Users, UsersTokensSalt, UsersRoles

from jwt import encode

from hashlib import md5

import random

from app.forms import is_form_valid

from app.controllers.secrets import JWT_SECRET, PASSWORD_SALT

from app.controllers.auth_controller import auth

from string import ascii_letters, digits

import re


# Генерация дополнительной соли для JWT токена
def generate_token_salt(user_id):
    pattern = '{}{}'.format(ascii_letters, digits)
    salt = ''.join([random.choice(pattern) for _ in range(7)])
    UsersTokensSalt.insert(user_id=user_id, salt=salt)
    return salt


# Генерация JWT токена
def generate_token(user_id, email):
    salt = generate_token_salt(user_id)
    return encode({'id': user_id, 'email': email, 'salt': salt}, JWT_SECRET, algorithm='HS256')


# Хэщирование пароля (для регистрации/авторизации через почту)
def hash_password(password):
    pass_bytes = (password + PASSWORD_SALT).encode()
    pass_md5 = md5(pass_bytes).hexdigest()
    return pass_md5


# Проверка валидности пароля при авторизации через почту
def check_password(email, password):
    true_password = getattr(Users.query.filter_by(email=email).first(), 'password', None)
    if true_password != hash_password(password):
        return False
    return True


# Проверка email на валидность
def check_email(email):
    if re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return True
    return False


def get_user_id():
    return auth.current_user()['id']


# Проверка почты на доступность для регистрации
def users_email_availability_check(email):
    if not check_email(email):
        return resp_wrong_email_format()
    if Users.query.filter_by(email=email).first():
        return resp_account_exists()
    return resp_ok()


# Регистрация через почту
def users_register_email(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    email = form.email.data.lower()
    if not check_email(email):
        return resp_wrong_email_format()
    if Users.query.filter_by(email=email).first():
        return resp_account_exists()
    hashed_password = hash_password(form.password.data)
    user_obj = Users.insert(email=email, password=hashed_password)
    user_id = user_obj.id
    UsersRoles.insert(user_id=user_id, role_id=1)
    return resp_ok({
        'id': user_id,
        'email': email,
        'token': generate_token(user_id, email),
    })


# Авторизация через почту
def users_auth_email(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    email = form.email.data.lower()
    if not check_email(email):
        return resp_wrong_email_format()
    user_obj = Users.query.filter_by(email=email).first()
    if not user_obj:
        return resp_account_not_exists()
    password = form.password.data
    if not check_password(email, password):
        return resp_wrong_password()
    return resp_ok({
        'id': user_obj.id,
        'email': email,
        'token': generate_token(user_obj.id, email),
    })


# Метод выхода из аккаунта
def users_logout():
    user_id = get_user_id()
    UsersTokensSalt.query.filter_by(salt=auth.current_user()['salt'], user_id=user_id).first().delete()
    return resp_ok()


# Смена пароля
def users_change_password(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    user_id = get_user_id()
    old_password = hash_password(form.old_password.data)
    new_password = hash_password(form.new_password.data)
    if not Users.query.filter_by(id=user_id, password=old_password).first():
        return resp_wrong_password()
    if old_password == new_password:
        return resp_old_password()
    Users.query.filter_by(id=user_id).first().update(password=new_password)
    for salt in UsersTokensSalt.query.filter_by(user_id=user_id, deleted=False).all():
        salt.delete()
    user_email = auth.current_user()['email']
    resp = {
        'id': user_id,
        'email': user_email,
        'token': generate_token(user_id, user_email)
    }
    return resp_ok(resp)


def check_token():
    user_id = get_user_id()
    return resp_ok({
        'id': user_id
    })
