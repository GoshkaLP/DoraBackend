from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, date

db = SQLAlchemy()


def get_current_datetime():
    current_datetime = datetime.combine(date.today(), datetime.min.time())
    return current_datetime


# Базовые функции для всех таблиц
class BaseFuncs(object):
    @classmethod
    def insert(cls, **kw):
        obj = cls(**kw)
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        self.update(deleted=True)


# Таблицы
class Users(BaseFuncs, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    verified = db.Column(db.Boolean, default=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class UsersCodes(BaseFuncs, db.Model):
    __tablename__ = 'users_codes'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class UsersTokensSalt(BaseFuncs, db.Model):
    __tablename__ = 'users_tokens_salt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    salt = db.Column(db.String(7))
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class WarrantiesCategories(BaseFuncs, db.Model):
    __tablename__ = 'warranties_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    type_warranty_period = db.Column(db.String(1))
    warranty_period = db.Column(db.Integer, nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class UsersWarranties(BaseFuncs, db.Model):
    __tablename__ = 'users_warranties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    shop_name = db.Column(db.String(255), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    date_of_purchase = db.Column(db.DateTime, nullable=False)
    type_warranty_period = db.Column(db.String(1))
    warranty_period = db.Column(db.Integer, nullable=False)
    archived = db.Column(db.Boolean, default=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class WarrantiesFiles(BaseFuncs, db.Model):
    __tablename__ = 'warranties_files'
    id = db.Column(db.Integer, primary_key=True)
    warranty_id = db.Column(db.Integer, nullable=False)
    path_to_file = db.Column(db.String(255), nullable=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)


class WarrantiesCases(BaseFuncs, db.Model):
    __tablename__ = 'warranties_cases'
    id = db.Column(db.Integer, primary_key=True)
    warranty_id = db.Column(db.Integer, nullable=False)
    expertise = db.Column(db.Boolean, nullable=False, default=False)
    date_end_expertise = db.Column(db.DateTime)
    money_returned = db.Column(db.Boolean, default=False)
    item_replaced = db.Column(db.Boolean, default=False)
    date_of_creation = db.Column(db.DateTime, nullable=False, default=get_current_datetime())
    deleted = db.Column(db.Boolean, default=False)
