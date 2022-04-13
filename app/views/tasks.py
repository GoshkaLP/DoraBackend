# from flask_apscheduler import APScheduler
#
# from .models import UsersCodes, UsersWarranties
#
# from .extensions.warranties_ext import get_date_and_days_end_warranty
#
# from datetime import datetime
#
# scheduler = APScheduler()
#
#
# # Обновление времени жизни кодов каждый день
# @scheduler.task('cron', id='do_update_codes', hour=0, minute=0)
# def update_codes():
#     with scheduler.app.app_context():
#         codes = UsersCodes.query.filter_by(deleted=False).all()
#         for code in codes:
#             code_date_of_creation = code.date_of_creation
#             now_date = datetime.now()
#             if (now_date - code_date_of_creation).days >= 1:
#                 code.delete()
#
#
# # Архивация истекших по времени талонов
# @scheduler.task('cron', id='do_archive_warranties', hour=0, minute=0)
# def archive_warranties():
#     with scheduler.app.app_context():
#         warranties = UsersWarranties.query.filter_by(deleted=False).all()
#         for warranty in warranties:
#             date_end_warranty, _ = get_date_and_days_end_warranty(warranty.type_warranty_period,
#                                                                   warranty.warranty_period, warranty.date_of_purchase)
#             if date_end_warranty < datetime.now():
#                 warranty.update(archived=True)
