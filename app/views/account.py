from flask import Blueprint

from .extensions.protection_ext import auth, api_users_register_email, api_users_auth_email, api_users_verify,\
    api_users_reset_get, api_users_reset_post, api_users_verify_resend, api_users_reset_code_check, api_users_logout,\
    api_users_change_password, api_users_token_check, api_users_email_availability_check

from .forms import RegisterAuthEmailForm, ResetPasswordForm, LogoutForm, ChangePasswordForm,\
    VerifyEmailForm

account = Blueprint('account', __name__)


@account.route('/api/users/register/email', methods=['POST'])
def route_api_users_register_email():
    form = RegisterAuthEmailForm()
    return api_users_register_email(form)


@account.route('/api/users/auth/email', methods=['POST'])
def route_api_users_auth_email():
    form = RegisterAuthEmailForm()
    return api_users_auth_email(form)


@account.route('/api/users/email/availability/check/<string:user_email>', methods=['GET'])
def route_api_users_email_availability_check(user_email):
    return api_users_email_availability_check(user_email)


@account.route('/api/users/<int:user_id>/token/check', methods=['GET'])
@auth.login_required
def route_api_users_token_check(user_id):
    return api_users_token_check(user_id)


@account.route('/api/users/verify', methods=['POST'])
@auth.login_required
def route_api_users_verify():
    form = VerifyEmailForm()
    return api_users_verify(form)


@account.route('/api/users/<int:user_id>/verify/resend', methods=['GET'])
@auth.login_required
def route_api_users_verify_resend(user_id):
    return api_users_verify_resend(user_id)


@account.route('/api/users/reset/<string:email>', methods=['GET'])
def route_api_users_reset_get(email):
    return api_users_reset_get(email)


@account.route('/api/users/reset/<string:email>/check/<int:code>', methods=['GET'])
def route_api_users_reset_code_check(email, code):
    return api_users_reset_code_check(email, code)


@account.route('/api/users/reset', methods=['POST'])
def route_api_users_reset_post():
    form = ResetPasswordForm()
    return api_users_reset_post(form)


@account.route('/api/users/logout', methods=['POST'])
@auth.login_required
def route_api_users_logout():
    form = LogoutForm()
    return api_users_logout(form)


@account.route('/api/users/change/password/email', methods=['POST'])
@auth.login_required
def route_api_users_change_password():
    form = ChangePasswordForm()
    return api_users_change_password(form)
