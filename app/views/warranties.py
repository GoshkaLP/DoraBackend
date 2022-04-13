from flask import Blueprint

from .extensions.protection_ext import auth

from .forms import WarrantyPostForm, WarrantyPatchForm, WarrantyDeleteForm

from .extensions.warranties_ext import api_warranties_categories, api_users_warranties_get,\
    api_users_file, api_users_warranties_post, api_users_warranties_delete, api_users_warranties_patch

warranties = Blueprint('warranties', __name__)


@warranties.route('/api/warranties/categories', methods=['GET'])
@auth.login_required
def route_api_categories():
    return api_warranties_categories()


@warranties.route('/api/users/warranties', methods=['POST'])
@auth.login_required
def route_api_users_warranties_post():
    form = WarrantyPostForm()
    return api_users_warranties_post(form)


@warranties.route('/api/users/warranties', methods=['PATCH'])
@auth.login_required
def route_api_users_warranties_patch():
    form = WarrantyPatchForm()
    return api_users_warranties_patch(form)


@warranties.route('/api/users/<int:user_id>/file/<int:file_id>', methods=['GET'])
@auth.login_required
def route_api_users_file(user_id, file_id):
    return api_users_file(user_id, file_id)


@warranties.route('/api/users/<int:user_id>/warranties', methods=['GET'])
@auth.login_required
def route_api_users_warranties_get(user_id):
    return api_users_warranties_get(user_id)


@warranties.route('/api/users/warranties', methods=['DELETE'])
@auth.login_required
def route_api_users_warranties_delete():
    form = WarrantyDeleteForm()
    return api_users_warranties_delete(form)
