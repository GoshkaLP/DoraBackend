from app.controllers.secrets import JWT_SECRET
from app.models import Users, UsersTokensSalt, UsersRoles

from jwt import decode
from jwt.exceptions import InvalidTokenError

from flask_httpauth import HTTPTokenAuth

from app.controllers.responses_controller import resp_wrong_token

# Authentication JWT settings
auth = HTTPTokenAuth(scheme='Bearer')


def get_user_role(user_id):
    user = UsersRoles.query.filter_by(user_id=user_id).first()
    return user.roles.name


@auth.get_user_roles
def get_role(user):
    return user['role']


@auth.verify_token
def verify_token(token):
    try:
        decode_data = decode(token, JWT_SECRET, algorithms=['HS256'])
        if decode_data.keys() == {'id', 'email', 'salt'} and \
                Users.query.filter_by(id=decode_data['id']).first() and \
                UsersTokensSalt.query.filter_by(salt=decode_data['salt'], deleted=False).first():
            decode_data.update({
                'role': get_user_role(decode_data['id'])
            })
            return decode_data
        pass
    except InvalidTokenError:
        pass


@auth.error_handler
def error_handler():
    return resp_wrong_token()
