from flask import Blueprint

from app.controllers.users_controller import auth, users_register_email, users_auth_email, \
    users_logout, users_change_password, users_email_availability_check, \
    check_token

from app.forms import RegisterAuthEmailForm, ChangePasswordForm

users = Blueprint('users', __name__)


@users.route('/api/users/register/email', methods=['POST'])
def api_users_register_email():
    form = RegisterAuthEmailForm()
    return users_register_email(form)


@users.route('/api/users/auth/email', methods=['POST'])
def api_users_auth_email():
    form = RegisterAuthEmailForm()
    return users_auth_email(form)


@users.route('/api/users/email/availability/check/<string:user_email>', methods=['GET'])
def api_users_email_availability_check(user_email):
    return users_email_availability_check(user_email)


@users.route('/api/users/logout', methods=['GET'])
@auth.login_required
def api_users_logout():
    return users_logout()


@users.route('/api/users/change/password/email', methods=['POST'])
@auth.login_required
def api_users_change_password():
    form = ChangePasswordForm()
    return users_change_password(form)


@users.route('/api/users/token/check', methods=['GET'])
@auth.login_required
def api_check_token():
    return check_token()
