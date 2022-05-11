# Шаблон ответа сервера на запрос
def generate_resp(status, message, data):
    return {
        'status': status,
        'message': message,
        'data': data
    }


# Ответы сервера
def resp_ok(data=None):
    if data is None:
        data = []
    return generate_resp('ok', 'SUCCESS', data), 200


def resp_form_not_valid():
    return generate_resp('error', 'FORM_NOT_VALID', []), 200


def resp_wrong_token():
    return generate_resp('error', 'WRONG_TOKEN', []), 200


def resp_wrong_email_format():
    return generate_resp('error', 'WRONG_EMAIL_FORMAT', []), 200


def resp_account_not_exists():
    return generate_resp('error', 'ACCOUNT_NOT_EXISTS', []), 200


def resp_account_exists():
    return generate_resp('error', 'ACCOUNT_ALREADY_EXISTS', []), 200


def resp_old_password():
    return generate_resp('error', 'OLD_PASSWORD', []), 200


def resp_wrong_password():
    return generate_resp('error', 'WRONG_PASSWORD', []), 200


def resp_manufacturer_exists():
    return generate_resp('error', 'MANUFACTURER_ALREADY_EXISTS', []), 200


def resp_manufacturer_not_exists():
    return generate_resp('error', 'MANUFACTURER_NOT_EXISTS', []), 200


def resp_product_type_exists():
    return generate_resp('error', 'PRODUCT_TYPE_ALREADY_EXISTS', 200), []


def resp_model_exists():
    return generate_resp('error', 'MODEL_ALREADY_EXISTS', []), 200


def resp_model_not_exists():
    return generate_resp('error', 'MODEL_NOT_EXISTS', []), 200


def resp_unit_exists():
    return generate_resp('error', 'UNIT_ALREADY_EXISTS', []), 200


def resp_unit_not_exists():
    return generate_resp('error', 'UNIT_NOT_EXISTS', []), 200


def resp_file_not_exists():
    return generate_resp('error', 'FILE_NOT_EXISTS', []), 200


def resp_wrong_qr_code():
    return generate_resp('error', 'WRONG_QR_CODE', []), 200


def resp_unit_assigned():
    return generate_resp('error', 'UNIT_ALREADY_ASSIGNED', []), 200


def resp_service_center_exists():
    return generate_resp('error', 'SERVICE_CENTER_ALREADY_EXISTS', []), 200


def resp_service_center_not_exists():
    return generate_resp('error', 'SERVICE_CENTER_NOT_EXISTS', []), 200


def resp_warranty_claim_exists():
    return generate_resp('error', 'WARRANTY_CLAIM_ALREADY_EXISTS', []), 200


def resp_wrong_unit_owner():
    return generate_resp('error', 'WRONG_UNIT_OWNER', []), 200


def resp_warranty_period_expired():
    return generate_resp('error', 'WARRANTY_PERIOD_EXPIRED', []), 200


def resp_warranty_claim_not_exists():
    return generate_resp('error', 'WARRANTY_CLAIM_NOT_EXISTS', []), 200
