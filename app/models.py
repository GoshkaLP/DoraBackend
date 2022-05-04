from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import BYTEA

from datetime import datetime

db = SQLAlchemy()


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
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    roles = db.relationship('UsersRoles', backref=db.backref('users'))
    tokens_salt = db.relationship('UsersTokensSalt', backref=db.backref('users'))
    units = db.relationship('CustomersProductUnit', backref=db.backref('users'))
    manufacturers = db.relationship('UsersManufacturers', backref=db.backref('users'))
    service_centers = db.relationship('UsersServiceCenter', backref=db.backref('users'))


class UsersTokensSalt(BaseFuncs, db.Model):
    __tablename__ = 'UsersTokensSalt'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    salt = db.Column(db.String(7), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class Roles(BaseFuncs, db.Model):
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    roles = db.relationship('UsersRoles', backref=db.backref('roles'))


class UsersRoles(BaseFuncs, db.Model):
    __tablename__ = 'UsersRoles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class Manufacturers(BaseFuncs, db.Model):
    __tablename__ = 'Manufacturers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    service_centers = db.relationship('ServiceCenter', backref=db.backref('manufacturer'))
    types = db.relationship('ProductTypes', backref=db.backref('manufacturer'))
    models = db.relationship('ProductModel', backref=db.backref('manufacturer'))
    users = db.relationship('UsersManufacturers', backref=db.backref('manufacturer'))


class UsersManufacturers(BaseFuncs, db.Model):
    __tablename__ = 'UsersManufacturers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Manufacturers.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class ProductTypes(BaseFuncs, db.Model):
    __tablename__ = 'ProductTypes'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Manufacturers.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    warranty_period = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    models = db.relationship('ProductModel', backref=db.backref('product_type'))


class ProductModel(BaseFuncs, db.Model):
    __tablename__ = 'ProductModel'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Manufacturers.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('ProductTypes.id'), nullable=False)
    photo = db.Column(BYTEA, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    units = db.relationship('ProductUnit', backref=db.backref('product_model'))


class ProductUnit(BaseFuncs, db.Model):
    __tablename__ = 'ProductUnit'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ProductModel.id'), nullable=False)
    serial_number = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(10), nullable=False)
    assigned = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    claims = db.relationship('WarrantyClaim', backref=db.backref('product_unit'))
    customers = db.relationship('CustomersProductUnit', backref=db.backref('product_unit'))
    warranties = db.relationship('WarrantyProductUnit', backref=db.backref('product_unit'))


class CustomersProductUnit(BaseFuncs, db.Model):
    __tablename__ = 'CustomersProductUnit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('ProductUnit.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class ServiceCenter(BaseFuncs, db.Model):
    __tablename__ = 'ServiceCenter'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('Manufacturers.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.DECIMAL, nullable=False)
    longitude = db.Column(db.DECIMAL, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)

    claims = db.relationship('WarrantyClaim', backref=db.backref('service_center'))
    users = db.relationship('UsersServiceCenter', backref=db.backref('service_center'))


class WarrantyClaim(BaseFuncs, db.Model):
    __tablename__ = 'WarrantyClaim'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('ProductUnit.id'), nullable=False)
    service_center_id = db.Column(db.Integer, db.ForeignKey('ServiceCenter.id'), nullable=False)
    problem = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='Создана')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class WarrantyProductUnit(BaseFuncs, db.Model):
    __tablename__ = 'WarrantyProductUnit'
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('ProductUnit.id'), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)


class UsersServiceCenter(BaseFuncs, db.Model):
    __tablename__ = 'UsersServiceCenter'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    service_center_id = db.Column(db.Integer, db.ForeignKey('ServiceCenter.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    deleted = db.Column(db.Boolean, default=False)
