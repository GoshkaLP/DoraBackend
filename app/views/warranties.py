from flask import Blueprint

from app.controllers.auth_controller import auth

from app.forms import CreateManufacturer, CreateProductType, \
    CreateModel, CreateUnit, AddCustomerUnit, CreateServiceCenter, \
    CreateWarrantyClaim, ChangeWarrantyClaim

from app.controllers.warranties_controller import create_manufacturer, create_product_type, \
    create_model, create_unit, get_manufacturers, get_models, get_units, \
    get_product_types, send_product_photo, send_qr_photo, add_customer_unit, \
    create_service_center, get_service_centers, create_warranty_claim, \
    change_warranty_claim_status, get_warranty_claims, get_warranty_claim_status, \
    get_unit

warranties = Blueprint('warranties', __name__)


@warranties.route('/api/manufacturers/create', methods=['POST'])
@auth.login_required(role='admin')
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
@auth.login_required(role='admin')
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


@warranties.route('/api/products/units/<int:unit_id>', methods=['GET'])
@auth.login_required(role='customer')
def api_get_unit(unit_id):
    return get_unit(unit_id)


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


@warranties.route('/api/serviceCenter/create', methods=['POST'])
@auth.login_required(role='manufacturer')
def api_create_service_center():
    form = CreateServiceCenter()
    return create_service_center(form)


@warranties.route('/api/serviceCenter', methods=['GET'])
@auth.login_required(role='manufacturer')
def api_get_service_centers_manufacturer():
    return get_service_centers()


@warranties.route('/api/serviceCenter/<int:manufacturer_id>', methods=['GET'])
@auth.login_required(role='customer')
def api_get_service_centers_customer(manufacturer_id):
    return get_service_centers(manufacturer_id)


@warranties.route('/api/warrantyClaim/create', methods=['POST'])
@auth.login_required(role='customer')
def api_create_warranty_claim():
    form = CreateWarrantyClaim()
    return create_warranty_claim(form)


@warranties.route('/api/warrantyClaim/status/<int:unit_id>', methods=['GET'])
@auth.login_required(role='customer')
def api_get_warranty_claim_status(unit_id):
    return get_warranty_claim_status(unit_id)


@warranties.route('/api/warrantyClaim', methods=['GET'])
@auth.login_required(role='service')
def api_get_warranty_claims():
    return get_warranty_claims()


@warranties.route('/api/warrantyClaim/status/change', methods=['POST'])
@auth.login_required(role='service')
def api_change_warranty_claim_status():
    form = ChangeWarrantyClaim()
    return change_warranty_claim_status(form)
