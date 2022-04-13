from flask import Blueprint

from .extensions.main_ext import generate_resp

# Для тестирования приложения
import re
from io import BytesIO
import requests as r
from flask import send_file
from os import path

node = Blueprint('node', __name__)


@node.route('/api/version', methods=['GET'])
def api_version():
    resp = {
        'version': '2.0.0',
        'server_status': 'working'
    }
    return generate_resp('ok', 'Success', resp)


def get_app_qr_code():
    pattern = re.compile('exp://.+:80')
    try:
        with open(path.join('/', 'var', 'log', 'expo.log'), 'r') as file:
            all_urls = pattern.findall(file.read())
    except:
        return None

    if not all_urls:
        return None

    app_url = all_urls[-1]
    qr_api_url = 'https://api.qrserver.com/v1/create-qr-code'
    params = {
        'size': '1000x1000',
        'data': app_url
    }

    try:
        req = r.get(qr_api_url, params=params)
        return BytesIO(req.content)
    except:
        return None


@node.route('/api/app/url', methods=['GET'])
def api_app_url_route():
    qr_obj = get_app_qr_code()
    if not qr_obj:
        return generate_resp('error', 'An error has occurred', [])
    return send_file(qr_obj, mimetype='image/png')
