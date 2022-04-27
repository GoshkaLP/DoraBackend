from flask import Blueprint

from app.controllers.users_controller import auth, api_users_register_email, api_users_auth_email, \
    api_users_logout, api_users_change_password, api_users_email_availability_check

from app.forms import RegisterAuthEmailForm, ChangePasswordForm

users = Blueprint('users', __name__)


@users.route('/api/users/register/email', methods=['POST'])
def route_api_users_register_email():
    form = RegisterAuthEmailForm()
    return api_users_register_email(form)


@users.route('/api/users/auth/email', methods=['POST'])
def route_api_users_auth_email():
    form = RegisterAuthEmailForm()
    return api_users_auth_email(form)


@users.route('/api/users/email/availability/check/<string:user_email>', methods=['GET'])
def route_api_users_email_availability_check(user_email):
    return api_users_email_availability_check(user_email)


@users.route('/api/users/logout', methods=['POST'])
@auth.login_required
def route_api_users_logout():
    return api_users_logout()


@users.route('/api/users/change/password/email', methods=['POST'])
@auth.login_required
def route_api_users_change_password():
    form = ChangePasswordForm()
    return api_users_change_password(form)
