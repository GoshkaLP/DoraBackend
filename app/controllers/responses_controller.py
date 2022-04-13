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
    return generate_resp('error', 'FORM_NOT_VALID', []), 400


def resp_wrong_token():
    return generate_resp('error', 'WRONG_TOKEN', []), 401


def resp_wrong_email_format():
    return generate_resp('error', 'WRONG_EMAIL_FORMAT', []), 400


def resp_wrong_code():
    return generate_resp('error', 'WRONG_CODE', []), 400


def resp_code_expires():
    return generate_resp('error', 'CODE_EXPIRES', []), 400


def resp_account_not_verified():
    return generate_resp('error', 'ACCOUNT_NOT_VERIFIED', []), 401


def resp_account_verified():
    return generate_resp('error', 'ACCOUNT_ALREADY_VERIFIED', []), 400


def resp_account_not_exists():
    return generate_resp('error', 'ACCOUNT_NOT_EXISTS', []), 400


def resp_account_exists():
    return generate_resp('error', 'ACCOUNT_ALREADY_EXISTS', []), 400


def resp_old_password():
    return generate_resp('error', 'OLD_PASSWORD', []), 400


def resp_wrong_password():
    return generate_resp('error', 'WRONG_PASSWORD', []), 401


def resp_freq_password_change():
    return generate_resp('error', 'FREQ_PASSWORD_CHANGE', []), 400


def resp_no_warranty():
    return generate_resp('error', 'NO_WARRANTY', []), 400


def resp_no_warranties():
    return generate_resp('error', 'NO_WARRANTIES', []), 400


def resp_no_file():
    return generate_resp('error', 'NO_FILE', []), 400


def resp_unable_to_save_file():
    return generate_resp('error', 'UNABLE_TO_SAVE_FILE', []), 400


def resp_unable_to_delete_file():
    return generate_resp('error', 'UNABLE_TO_DELETE_FILE', []), 400
