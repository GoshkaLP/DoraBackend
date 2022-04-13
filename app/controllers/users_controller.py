from flask_httpauth import HTTPTokenAuth

from flask_mail import Mail

from app.controllers.responses_controller import resp_ok, resp_wrong_code, resp_wrong_token, resp_account_exists, resp_account_not_exists, \
    resp_account_verified, resp_code_expires, resp_old_password, resp_wrong_password, resp_form_not_valid, \
    resp_account_not_verified, resp_wrong_email_format, resp_freq_password_change

from app.models import Users, UsersCodes, UsersTokensSalt

from jwt import decode, encode
from jwt.exceptions import InvalidTokenError

from hashlib import md5

import random

from app.controllers.secrets import JWT_SECRET, PASSWORD_SALT

from string import ascii_letters, digits


import re

from datetime import datetime


# Authentication JWT settings
auth = HTTPTokenAuth(scheme='Bearer')

# Объект почты
mail = Mail()


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


@auth.verify_token
def verify_token(token):
    try:
        decode_data = decode(token, JWT_SECRET, algorithms=['HS256'])
        if decode_data.keys() == {'id', 'email', 'salt'} and \
                Users.query.filter_by(id=decode_data['id']).first() and \
                UsersTokensSalt.query.filter_by(salt=decode_data['salt'], deleted=False).first():
            return decode_data
        pass
    except InvalidTokenError:
        pass


@auth.error_handler
def error_handler():
    return resp_wrong_token()


# Проверка валидность формы
def is_form_valid(form):
    return form.validate_on_submit()


# Проверка верифицированности пользователя
def is_user_verified(user_id):
    verified = Users.query.filter_by(id=user_id).first().verified
    return verified


# Проверка совпадения id пользователя, переданного в токене и в теле запроса
def is_user_id_correct(user_id_from_method, user_id_from_token):
    return user_id_from_method == user_id_from_token


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


# Генерация кода для верификации или сброса пароля
def generate_code(email, code_type):
    code = random.randint(1000, 9999)
    UsersCodes.insert(email=email, type=code_type, code=code)
    return code


# Проверка токена на валидность
def api_users_token_check(user_id):
    if not is_user_id_correct(user_id, auth.current_user()['id']):
        return resp_wrong_token()
    resp = {
        'id': user_id,
        'email': auth.current_user()['email'],
        'verified': Users.query.filter_by(id=user_id).first().verified
    }
    return resp_ok(resp)


# Верификация аккаунта
def api_users_verify(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    user_id = form.user_id.data
    if not is_user_id_correct(user_id, auth.current_user()['id']):
        return resp_wrong_token()
    email = auth.current_user()['email']
    if not check_email(email):
        return resp_wrong_email_format()
    if is_user_verified(user_id):
        return resp_account_verified()
    code = form.code.data
    obj = UsersCodes.query.filter_by(type=0, email=email, code=code).first()
    if not obj:
        return resp_wrong_code()
    if obj.deleted:
        return resp_code_expires()
    Users.query.filter_by(email=email).first().update(verified=True)
    return resp_ok()


# Отправка письма с подтверждением регистрации
def send_verification_mail(email):
    # todo переработать текста
    verify_code = generate_code(email, 0)
    subject = 'Dora Team'
    message = 'Спасибо за регистрацию в нашем приложении.\n' \
              'Для завершения регистрации, введите следующий код в приложении:\n' \
              '{}'.format(verify_code)
    mail.send_message(subject=subject, body=message,
                      recipients=[email])


# Отправка письма для сброса пароля
def send_reset_password_mail(email):
    # todo переработать текста
    reset_code = generate_code(email, 1)
    subject = 'Dora Team'
    message = 'Вы запросили сброс пароля.\n' \
              'Укажите данный код в приложении:\n' \
              '{}'.format(reset_code)
    mail.send_message(subject=subject, body=message,
                      recipients=[email])


# Сброс пароля
def api_users_reset_post(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    email = form.email.data
    if not check_email(email):
        return resp_wrong_email_format()
    obj = Users.query.filter_by(email=email).first()
    if not obj:
        return resp_account_not_exists()
    code = form.code.data
    code_obj = UsersCodes.query.filter_by(email=email, type=1, code=code, deleted=False).first()
    if not code_obj:
        return resp_wrong_code()
    if code_obj.deleted:
        return resp_code_expires()
    new_password = hash_password(form.password.data)
    if obj.password == new_password:
        return resp_old_password()
    user_obj = Users.query.filter_by(email=email).first()
    user_obj.update(password=new_password)
    for salt in UsersTokensSalt.query.filter_by(user_id=user_obj.id, deleted=False).all():
        salt.delete()
    return resp_ok()


# Запрос кода для сброса пароля
def api_users_reset_get(email):
    if not check_email(email):
        return resp_wrong_email_format()
    obj = Users.query.filter_by(email=email).first()
    if not obj:
        return resp_account_not_exists()
    last_code = UsersCodes.query.filter_by(email=email, deleted=False, type=1).\
        order_by(UsersCodes.id.desc()).first()
    if last_code and (datetime.now() - last_code.date_of_creation).seconds // 60 < 1:
        return resp_freq_password_change()
    send_reset_password_mail(email)
    return resp_ok()


# Проверка кода сброса пароля
def api_users_reset_code_check(email, code):
    if not check_email(email):
        return resp_wrong_email_format()
    code_obj = UsersCodes.query.filter_by(email=email, type=1, code=code, deleted=False).first()
    if not code_obj:
        return resp_wrong_code()
    if code_obj.deleted:
        return resp_code_expires()
    return resp_ok()


# Смена пароля
def api_users_change_password(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    user_id = form.user_id.data
    if not is_user_id_correct(user_id, auth.current_user()['id']):
        return resp_wrong_token()
    if not is_user_verified(user_id):
        return resp_account_not_verified()
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
        'token': generate_token(user_id, user_email),
        'verified': Users.query.filter_by(id=user_id).first().verified
    }
    return resp_ok(resp)


# Register/Auth функции
# Проверка почты на доступность для регистрации
def api_users_email_availability_check(email):
    if not check_email(email):
        return resp_wrong_email_format()
    if Users.query.filter_by(email=email).first():
        return resp_account_exists()
    return resp_ok()


# Регистрация через почту
def api_users_register_email(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    email = form.email.data.lower()
    if not check_email(email):
        return resp_wrong_email_format()
    if Users.query.filter_by(email=email).first():
        return resp_account_exists()
    hashed_password = hash_password(form.password.data)
    user_obj = Users.insert(email=email, password=hashed_password)
    send_verification_mail(email)
    user_id = user_obj.id
    return resp_ok({
        'id': user_id,
        'email': email,
        'token': generate_token(user_id, email),
        'verified': user_obj.verified
    })


# Выслать запрос верификации повторно
def api_users_verify_resend(user_id):
    if not is_user_id_correct(user_id, auth.current_user()['id']):
        return resp_wrong_token()
    email = auth.current_user()['email']
    if not check_email(email):
        return resp_wrong_email_format()
    if is_user_verified(user_id):
        return resp_account_verified()
    send_verification_mail(email)
    return resp_ok()


# Авторизация через почту
def api_users_auth_email(form):
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
        'verified': user_obj.verified
    })


# Метод выхода из аккаунта
def api_users_logout(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    user_id = form.user_id.data
    if not is_user_id_correct(user_id, auth.current_user()['id']):
        return resp_wrong_token()
    UsersTokensSalt.query.filter_by(salt=auth.current_user()['salt'], user_id=user_id).first().delete()
    return resp_ok()
