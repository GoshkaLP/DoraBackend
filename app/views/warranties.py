from flask import Blueprint

from app.controllers.auth_controller import auth

from app.forms import CreateManufacturer, CreateProductType, \
    CreateModel, CreateUnit, AddCustomerUnit

from app.controllers.warranties_controller import create_manufacturer, create_product_type, \
    create_model, create_unit, get_manufacturers, get_models, get_units, \
    get_product_types, send_product_photo, send_qr_photo, add_customer_unit

warranties = Blueprint('warranties', __name__)


@warranties.route('/api/manufacturers/create', methods=['POST'])
@auth.login_required(role='manufacturer')
def api_create_manufacturer():
    form = CreateManufacturer()
    return create_manufacturer(form)


@warranties.route('/api/products/types/create', methods=['POST'])
@auth.login_required(role='manufacturer')
def api_create_product_type():
    form = CreateProductType()
    return create_product_type(form)


@warranties.route('/api/products/models/create', methods=['POST'])
@auth.login_required(role='manufacturer')
def api_create_product_model():
    form = CreateModel()
    return create_model(form)


@warranties.route('/api/products/units/create', methods=['POST'])
@auth.login_required(role='manufacturer')
def api_create_product_unit():
    form = CreateUnit()
    return create_unit(form)


@warranties.route('/api/manufacturers', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_manufacturers():
    return get_manufacturers()


@warranties.route('/api/products/models', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_models():
    return get_models()


@warranties.route('/api/products/units', methods=['GET'])
@auth.login_required(role=['manufacturer', 'customer'])
def api_get_units():
    return get_units()


@warranties.route('/api/products/types', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_product_types():
    return get_product_types()


@warranties.route('/api/products/models/photo/<int:model_id>', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_model_photo(model_id):
    return send_product_photo(model_id=model_id)


@warranties.route('/api/products/units/photo/<int:unit_id>', methods=['GET'])
@auth.login_required(role='customer')
def api_get_unit_photo(unit_id):
    return send_product_photo(unit_id=unit_id)


@warranties.route('/api/products/units/qr/<int:unit_id>', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_unit_qr(unit_id):
    return send_qr_photo(unit_id)


@warranties.route('/api/products/units/scan', methods=['POST'])
@auth.login_required(role='customer')
def api_add_customer_unit():
    form = AddCustomerUnit()
    return add_customer_unit(form)
