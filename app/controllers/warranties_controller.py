# from ..models import db, WarrantiesCategories, UsersWarranties, WarrantiesCases, WarrantiesFiles
#
# from .responses_controller import resp_ok, resp_account_not_verified, resp_wrong_token, resp_no_file, resp_no_warranty,\
#     resp_form_not_valid, resp_no_warranties, resp_unable_to_delete_file, resp_unable_to_save_file
#
# from .users_controller import auth, is_user_id_correct, is_user_verified, is_form_valid
#
# from .vars import DOMAIN
#
# from ..forms import DefaultFormValue
#
# from flask import send_file
#
# from os import path, getcwd, makedirs
#
# from dateutil.relativedelta import relativedelta
#
# from datetime import datetime
#
# from PIL import Image
#
#
# def get_new_file_size(sz):
#     x, y = sz
#     coefficient = 1
#     if max(x, y) > 2048:
#         coefficient = round(max(x, y) / 2048)
#     return round(x / coefficient), round(y / coefficient)
#
#
# def save_file(counter, warranty_id, user_path, file):
#     file_name = '{}_{}.jpg'.format(warranty_id, counter)
#     try:
#         save_path = path.join(user_path, file_name)
#         img = Image.open(file)
#         img = img.resize(get_new_file_size(img.size), Image.LANCZOS)
#         img.save(save_path, quality=90, optimize=True)
#         WarrantiesFiles.insert(path_to_file=file_name, warranty_id=warranty_id)
#         return True
#     except Exception:
#         return False
#
#
# def delete_file(file_obj):
#     if not file_obj:
#         return False
#     file_obj.delete()
#     return True
#
#
# def get_date_and_days_end_warranty(type_warranty_period, warranty_period, date_of_purchase):
#     add_value = relativedelta()
#     if type_warranty_period == 'D':
#         add_value.__init__(days=warranty_period)
#     elif type_warranty_period == 'M':
#         add_value.__init__(months=warranty_period)
#     elif type_warranty_period == 'Y':
#         add_value.__init__(years=warranty_period)
#     date_end_warranty = date_of_purchase + add_value
#     days_end_warranty = (datetime.now() - date_end_warranty).days * (-1)
#     if days_end_warranty < 0:
#         days_end_warranty = 0
#     return date_end_warranty, days_end_warranty
#
#
# def get_warranty_full_info(warranty_obj, cases_obj, files_obj):
#     date_end_warranty, days_end_warranty = get_date_and_days_end_warranty(warranty_obj.type_warranty_period,
#                                                                           warranty_obj.warranty_period,
#                                                                           warranty_obj.date_of_purchase)
#     info = {
#         'id': warranty_obj.id,
#         'name': warranty_obj.name,
#         'shop_name': warranty_obj.shop_name,
#         'category_id': warranty_obj.category_id,
#         'date_of_purchase': warranty_obj.date_of_purchase,
#         'date_end_warranty': date_end_warranty,
#         'days_end_warranty': days_end_warranty,
#         'files': [],
#         'expertise': cases_obj.expertise,
#         'date_end_expertise': cases_obj.date_end_expertise,
#         'money_returned': cases_obj.money_returned,
#         'item_replaced': cases_obj.item_replaced
#     }
#     for file in files_obj:
#         info['files'].append({
#             'file_id': file.id,
#             'file_url': '{}/api/users/{}/file/{}'.format(DOMAIN, warranty_obj.user_id, file.id)
#         })
#     return info
#
#
# # Метод выгрузки всех доступных категорий
# def api_warranties_categories():
#     if not is_user_verified(auth.current_user()['id']):
#         return resp_account_not_verified()
#     categories = WarrantiesCategories.query.all()
#     resp = []
#     for category in categories:
#         resp.append({
#             'category_id': category.id,
#             'category_name': category.name,
#             'type_warranty_period': category.type_warranty_period,
#             'warranty_period': category.warranty_period
#         })
#     return resp_ok(resp)
#
#
# # Метод добавление талона в базу
# def api_users_warranties_post(form):
#     if not is_form_valid(form):
#         return resp_form_not_valid()
#     user_id = form.user_id.data
#     email = auth.current_user()['email']
#     if not is_user_id_correct(user_id, auth.current_user()['id']):
#         return resp_wrong_token()
#     if not is_user_verified(user_id):
#         return resp_account_not_verified()
#     name = form.name.data
#     shop_name = form.shop_name.data
#     category_id = form.category_id.data
#     date_of_purchase = datetime.combine(form.date_of_purchase.data, datetime.min.time())
#     type_warranty_period = form.type_warranty_period.data
#     warranty_period = form.warranty_period.data
#     files = form.files.data
#     user_path = path.join(getcwd(), 'data', email)
#     archived = False
#     _, days_end_warranty = get_date_and_days_end_warranty(type_warranty_period, warranty_period, date_of_purchase)
#     if days_end_warranty == 0:
#         archived = True
#     if not path.exists(user_path):
#         makedirs(user_path)
#     warranty = UsersWarranties.insert(user_id=user_id, name=name, shop_name=shop_name,
#                                       category_id=category_id, date_of_purchase=date_of_purchase,
#                                       type_warranty_period=type_warranty_period, warranty_period=warranty_period,
#                                       archived=archived)
#     WarrantiesCases.insert(warranty_id=warranty.id)
#     for counter, file in enumerate(files, 1):
#         if not save_file(counter, warranty.id, user_path, file):
#             for file_obj in WarrantiesFiles.filter_by(warranty_id=warranty.id).all():
#                 delete_file(file_obj)
#             warranty.delete()
#             return resp_unable_to_save_file()
#     return resp_ok({'warranty_id': warranty.id})
#
#
# # Метод выгрузки всех талонов на пользователя
# def api_users_warranties_get(user_id):
#     if not is_user_id_correct(user_id, auth.current_user()['id']):
#         return resp_wrong_token()
#     if not is_user_verified(user_id):
#         return resp_account_not_verified()
#     warranties = UsersWarranties.query.filter_by(user_id=user_id, deleted=False).all()
#     if not warranties:
#         return resp_no_warranties()
#     archived = []
#     non_archived = []
#     for warranty in warranties:
#         files = WarrantiesFiles.query.filter_by(warranty_id=warranty.id, deleted=False).all()
#         cases = WarrantiesCases.query.filter_by(warranty_id=warranty.id).first()
#         warranty_info = get_warranty_full_info(warranty, cases, files)
#         if not warranty.archived:
#             non_archived.append(warranty_info)
#         else:
#             archived.append(warranty_info)
#     resp = {'non_archived': non_archived, 'archived': archived}
#     return resp_ok(resp)
#
#
# # Метод удаления талона пользователя
# def api_users_warranties_delete(form):
#     if not is_form_valid(form):
#         return resp_form_not_valid()
#     user_id = form.user_id.data
#     if not is_user_id_correct(user_id, auth.current_user()['id']):
#         return resp_wrong_token()
#     if not is_user_verified(user_id):
#         return resp_account_not_verified()
#     warranty_id = form.warranty_id.data
#     warranty = UsersWarranties.query.filter_by(id=warranty_id, deleted=False, user_id=user_id).first()
#     if not warranty:
#         return resp_no_warranty()
#     files = WarrantiesFiles.query.filter_by(warranty_id=warranty_id, deleted=False).all()
#     for file in files:
#         if not delete_file(file):
#             return resp_unable_to_delete_file()
#     warranty.delete()
#     WarrantiesCases.query.filter_by(warranty_id=warranty_id).first().delete()
#     return resp_ok()
#
#
# # Метод изменения талона пользователя
# def api_users_warranties_patch(form):
#     if not is_form_valid(form):
#         return resp_form_not_valid()
#     user_id = form.user_id.data
#     if not is_user_id_correct(user_id, auth.current_user()['id']):
#         return resp_wrong_token()
#     if not is_user_verified(user_id):
#         return resp_account_not_verified()
#     warranty_id = form.warranty_id.data
#     warranty_main = UsersWarranties.query.filter_by(id=warranty_id, deleted=False, user_id=user_id).first()
#     if not warranty_main:
#         return resp_no_warranty()
#     warranty_cases = WarrantiesCases.query.filter_by(warranty_id=warranty_id).first()
#     user_path = path.join(getcwd(), 'data', auth.current_user()['email'])
#     main_upd = {}
#     cases_upd = {}
#     warranty_main_params = {'name', 'shop_name', 'category_id', 'date_of_purchase',
#                             'type_warranty_period', 'warranty_period', 'archived'}
#     warranty_cases_params = {'expertise', 'date_end_expertise', 'money_returned', 'item_replaced'}
#     for key, value in form.data.items():
#         if key == 'files_delete' and value:
#             for file_id in value:
#                 file_obj = WarrantiesFiles.query.filter_by(id=file_id, deleted=False).first()
#                 if not delete_file(file_obj):
#                     return resp_unable_to_delete_file()
#         elif key == 'files_add' and value:
#             filename_counter = 1
#             last_file_obj = WarrantiesFiles.query.filter_by(warranty_id=warranty_id).\
#                 order_by(WarrantiesFiles.id.desc()).first()
#             last_file_path = getattr(last_file_obj, 'path_to_file', None)
#             if last_file_path:
#                 filename_counter = int(last_file_path[last_file_path.index('_')+1:last_file_path.index('.')]) + 1
#             for counter, file in enumerate(value, filename_counter):
#                 if not save_file(counter, warranty_id, user_path, file):
#                     return resp_unable_to_save_file()
#         elif key in warranty_main_params and not isinstance(value, DefaultFormValue):
#             main_upd.update({key: value})
#         elif key in warranty_cases_params and not isinstance(value, DefaultFormValue):
#             cases_upd.update({key: value})
#     if main_upd:
#         warranty_main.update(**main_upd)
#     if cases_upd:
#         if cases_upd.get('money_returned', False):
#             warranty_main.update(archived=True)
#         if cases_upd.get('item_replaced', False):
#             warranty_main.update(archived=True)
#         warranty_cases.update(**cases_upd)
#     warranty_files = WarrantiesFiles.query.filter_by(warranty_id=warranty_id, deleted=False).all()
#     resp = get_warranty_full_info(warranty_main, warranty_cases, warranty_files)
#     return resp_ok(resp)
#
#
# # Метод отправки фото с сервера
# def api_users_file(user_id, file_id):
#     if not is_user_id_correct(user_id, auth.current_user()['id']):
#         return resp_wrong_token()
#     if not is_user_verified(user_id):
#         return resp_account_not_verified()
#     file_obj = db.session.query(WarrantiesFiles.id, WarrantiesFiles.path_to_file,
#                                 UsersWarranties.user_id, WarrantiesFiles.deleted).\
#         join(UsersWarranties, UsersWarranties.id == WarrantiesFiles.warranty_id).\
#         filter(WarrantiesFiles.id == file_id, WarrantiesFiles.deleted == False).first()
#     if not file_obj:
#         return resp_no_file()
#     full_path = path.join(getcwd(), 'data', auth.current_user()['email'], file_obj.path_to_file)
#     if not path.exists(full_path):
#         return resp_no_file()
#     return send_file(full_path)
