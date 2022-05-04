from app.controllers.responses_controller import resp_ok, resp_form_not_valid, \
    resp_manufacturer_exists, resp_manufacturer_not_exists, resp_product_type_exists, \
    resp_model_exists, resp_model_not_exists, resp_unit_exists, resp_file_not_exists, \
    resp_wrong_qr_code, resp_unit_assigned, resp_service_center_exists, \
    resp_warranty_claim_exists, resp_wrong_unit_owner, resp_warranty_period_expired, \
    resp_service_center_not_exists, resp_warranty_claim_not_exists

from app.controllers.auth_controller import auth

from app.controllers.qr_controller import generate_qr, decode_qr

from app.forms import is_form_valid

from app.models import Manufacturers, ProductTypes, ProductModel, \
    ProductUnit, UsersManufacturers, CustomersProductUnit, \
    WarrantyProductUnit, ServiceCenter, WarrantyClaim, \
    UsersServiceCenter

from string import ascii_letters, digits

from flask import send_file

from sqlalchemy import desc

import random

from io import BytesIO

from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.controllers.secrets import BASE_URL


def get_user_id():
    user_id = auth.current_user()['id']
    return user_id


def get_manufacturer_id():
    user_id = get_user_id()
    user = UsersManufacturers.query.filter_by(user_id=user_id).first()
    return user.manufacturer_id


def get_service_center_id():
    user_id = get_user_id()
    user = UsersServiceCenter.query.filter_by(user_id=user_id).first()
    return user.service_center_id


def create_manufacturer(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    manufacturer_name = form.name.data
    if Manufacturers.query.filter_by(name=manufacturer_name).first():
        return resp_manufacturer_exists()
    manufacturer = Manufacturers.insert(name=manufacturer_name)
    resp = {
        'id': manufacturer.id
    }
    return resp_ok(resp)


def create_product_type(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    manufacturer_id = get_manufacturer_id()
    type_name = form.name.data
    warranty_period = form.warranty_period.data
    if not Manufacturers.query.filter_by(id=manufacturer_id).first():
        return resp_manufacturer_not_exists()
    if ProductTypes.query.filter_by(name=type_name, manufacturer_id=manufacturer_id).first():
        return resp_product_type_exists()
    product_type = ProductTypes.insert(
        manufacturer_id=manufacturer_id,
        name=type_name,
        warranty_period=warranty_period
    )
    resp = {
        'id': product_type.id
    }
    return resp_ok(resp)


def create_model(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    manufacturer_id = get_manufacturer_id()
    model_name = form.model_name.data
    type_id = form.product_type_id.data
    photo = form.photo.data
    if ProductModel.query.filter_by(name=model_name, manufacturer_id=manufacturer_id).first():
        return resp_model_exists()
    model = ProductModel.insert(
        manufacturer_id=manufacturer_id,
        name=model_name,
        product_type_id=type_id,
        photo=photo.read()
    )
    resp = {
        'id': model.id
    }
    return resp_ok(resp)


def generate_unit_salt():
    pattern = '{}{}'.format(ascii_letters, digits)
    salt = ''.join([random.choice(pattern) for _ in range(10)])
    return salt


def create_unit(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    model_id = form.model_id.data
    serial_number = form.serial_number.data
    if ProductUnit.query.filter_by(serial_number=serial_number).first():
        return resp_unit_exists()
    model = ProductModel.query.filter_by(id=model_id).first()
    if not model:
        return resp_model_not_exists()
    units = getattr(model, 'units', [])
    units.append(ProductUnit(
        model_id=model_id,
        serial_number=serial_number,
        salt=generate_unit_salt()
    ))
    model.update(units=units)
    return resp_ok()


def get_manufacturers():
    data = Manufacturers.query.all()
    resp = []
    for el in data:
        resp.append({
            'id': el.id,
            'name': el.name
        })
    return resp_ok(resp)


def get_models():
    manufacturer_id = get_manufacturer_id()
    data = ProductModel.query.filter_by(manufacturer_id=manufacturer_id).all()
    resp = []
    for model in data:
        resp.append({
            'id': model.id,
            'name': model.name,
            'type': model.product_type.name,
            'photo': '{url}/api/products/models/photo/{id}'.format(
                url=BASE_URL,
                id=model.id
            )
        })
    return resp_ok(resp)


def get_units():
    user_role = auth.current_user()['role']
    resp = []
    if user_role == 'manufacturer':
        manufacturer_id = get_manufacturer_id()
        data = ProductUnit.query. \
            join(ProductModel).filter(ProductModel.manufacturer_id == manufacturer_id).all()
        for unit in data:
            resp.append({
                'id': unit.id,
                'manufacturer': unit.product_model.manufacturer.name,
                'model': unit.product_model.name,
                'serialNumber': unit.serial_number,
                'assigned': unit.assigned,
                'qrImage': '{url}/api/products/units/qr/{id}'.format(
                    url=BASE_URL,
                    id=unit.id
                )
            })
    elif user_role == 'customer':
        user_id = get_user_id()
        data = ProductUnit.query. \
            join(CustomersProductUnit).filter(CustomersProductUnit.user_id == user_id).all()
        for unit in data:
            claimable = unit.warranties[0].end_date.date() > datetime.utcnow().date()
            resp.append({
                'id': unit.id,
                'manufacturer': unit.product_model.manufacturer.name,
                'manufacturerId': unit.product_model.manufacturer.id,
                'model': unit.product_model.name,
                'serialNumber': unit.serial_number,
                'warrantyEndDate': unit.warranties[0].end_date,
                'claimable': claimable,
                'photo': '{url}/api/products/units/photo/{id}'.format(
                    url=BASE_URL,
                    id=unit.id
                )
            })
    return resp_ok(resp)


def get_product_types():
    resp = []
    manufacturer_id = get_manufacturer_id()
    data = ProductTypes.query.filter_by(manufacturer_id=manufacturer_id).all()
    for pr_type in data:
        resp.append({
            'id': pr_type.id,
            'name': pr_type.name
        })
    return resp_ok(resp)


def send_qr_photo(unit_id):
    manufacturer_id = get_manufacturer_id()
    data = ProductUnit.query \
        .join(ProductModel).filter(
            ProductModel.manufacturer_id == manufacturer_id, ProductUnit.id == unit_id
    ).first()
    if data:
        img = generate_qr(data.salt, data.id)
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        return send_file(
            img_bytes,
            mimetype='image/jpeg',
            as_attachment=True,
            attachment_filename='photo.jpg'
        )
    return resp_file_not_exists()


def send_product_photo(model_id=None, unit_id=None):
    img = None
    if model_id:
        manufacturer_id = get_manufacturer_id()
        data = ProductModel.query.filter_by(id=model_id,
                                            manufacturer_id=manufacturer_id).first()
        if not data:
            return resp_file_not_exists()
        img = data.photo
    elif unit_id:
        user_id = get_user_id()
        data = ProductUnit.query. \
            join(CustomersProductUnit).filter(
                CustomersProductUnit.user_id == user_id, ProductUnit.id == unit_id
        ).first()
        if not data:
            return resp_file_not_exists()
        img = data.product_model.photo
    else:
        return resp_file_not_exists()

    return send_file(
        BytesIO(img),
        mimetype='image/jpeg',
        as_attachment=True,
        attachment_filename='photo.jpg'
    )


def add_customer_unit(form):
    user_id = get_user_id()
    qr_data = form.qr.data
    decoded_data = decode_qr(qr_data)
    if not decoded_data:
        return resp_wrong_qr_code()
    unit_id = decoded_data['unit_id']
    salt = decoded_data['salt']
    unit = ProductUnit.query.filter_by(id=unit_id, salt=salt).first()
    if not unit:
        return resp_wrong_qr_code()
    if unit.assigned:
        return resp_unit_assigned()
    if CustomersProductUnit.query.filter_by(user_id=user_id, unit_id=unit_id).first():
        return resp_unit_assigned()
    CustomersProductUnit.insert(user_id=user_id, unit_id=unit_id)
    warranty_period = unit.product_model.product_type.warranty_period
    WarrantyProductUnit.insert(
        unit_id=unit_id,
        end_date=datetime.utcnow() + relativedelta(months=warranty_period)
    )
    unit.update(assigned=True)
    return resp_ok()


def create_service_center(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    manufacturer_id = get_manufacturer_id()
    name = form.name.data
    if ServiceCenter.query.filter_by(manufacturer_id=manufacturer_id, name=name).first():
        return resp_service_center_exists()
    latitude, longitude = form.coordinates.data
    address = form.address.data
    service = ServiceCenter.insert(
        manufacturer_id=manufacturer_id,
        name=name,
        latitude=latitude,
        longitude=longitude,
        address=address
    )
    return resp_ok({
        'id': service.id
    })


def get_service_centers(manufacturer_id=None):
    if not manufacturer_id:
        manufacturer_id = get_manufacturer_id()
    data = ServiceCenter.query.filter_by(manufacturer_id=manufacturer_id).all()
    resp = []
    for service in data:
        resp.append({
            'id': service.id,
            'manufacturer': service.manufacturer.name,
            'name': service.name,
            'address': service.address,
            'coordinates': (service.latitude, service.longitude)
        })
    return resp_ok(resp)


def create_warranty_claim(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    user_id = get_user_id()
    unit_id = form.unit_id.data
    unit = ProductUnit.query. \
        join(CustomersProductUnit).filter(CustomersProductUnit.user_id == user_id,
                                          CustomersProductUnit.unit_id == unit_id).first()
    if not unit:
        return resp_wrong_unit_owner()
    claimable = unit.warranties[0].end_date.date() > datetime.utcnow().date()
    if not claimable:
        return resp_warranty_period_expired()
    if WarrantyClaim.query.filter(WarrantyClaim.unit_id == unit_id, WarrantyClaim.status != "Закрыта").first():
        return resp_warranty_claim_exists()
    service_center_id = form.service_center_id.data
    if not ServiceCenter.query.filter_by(id=service_center_id).first():
        return resp_service_center_not_exists()
    problem = form.problem.data
    claim = WarrantyClaim.insert(
        unit_id=unit_id,
        service_center_id=service_center_id,
        problem=problem
    )
    return resp_ok({
        'id': claim.id
    })


def get_warranty_claims():
    service_center_id = get_service_center_id()
    data = WarrantyClaim.query.filter(WarrantyClaim.service_center_id == service_center_id,
                                      WarrantyClaim.status != 'Закрыта').all()
    resp = []
    for claim in data:
        resp.append({
            'id': claim.id,
            'status': claim.status,
            'unit_id': claim.unit_id,
            'problem': claim.problem
        })
    return resp_ok(resp)


def change_warranty_claim_status(form):
    if not is_form_valid(form):
        return resp_form_not_valid()
    service_center_id = get_service_center_id()
    claim_id = form.claim_id.data
    claim = WarrantyClaim.query.filter(WarrantyClaim.id == claim_id, WarrantyClaim.status != 'Закрыта',
                                       WarrantyClaim.service_center_id == service_center_id).first()
    if not claim:
        return resp_warranty_claim_not_exists()
    status = form.status.data
    claim.update(status=status)
    return resp_ok()


def get_warranty_claim_status(unit_id):
    user_id = get_user_id()
    claim = WarrantyClaim.query.join(ProductUnit, CustomersProductUnit). \
        filter(ProductUnit.id == unit_id, CustomersProductUnit.user_id == user_id,
               WarrantyClaim.status != 'Закрыта').\
        order_by(desc(WarrantyClaim.created_at)).first()
    if not claim:
        return resp_warranty_claim_not_exists()
    return resp_ok({
        'status': claim.status
    })
