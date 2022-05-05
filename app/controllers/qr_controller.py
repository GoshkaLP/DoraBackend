from qrcode import QRCode, constants

from PIL import Image

from json import dumps, loads

from os import path, getcwd

import base64


def generate_qr(salt, unit_id):
    logo_path = path.join(getcwd(), 'app', 'static', 'dora.png')
    # logo_path = 'C:\\Users\\rybki\\stuff\\DoraBackend\\static\\dora.png'
    logo = Image.open(logo_path)
    data = {
        'salt': salt,
        'unit_id': unit_id
    }

    encoded_data = base64.b64encode(dumps(data).encode()).decode()
    print(encoded_data)

    qr = QRCode(error_correction=constants.ERROR_CORRECT_H)
    qr.add_data(encoded_data)
    img = qr.make_image(fill_color=(0, 122, 255), back_color='white')
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)

    img.paste(logo, pos, logo)
    return img


def decode_qr(data):
    try:
        decoded_data = loads(base64.b64decode(data).decode())
        if list(decoded_data.keys()) == ['salt', 'unit_id']:
            return decoded_data
        return None
    except:
        return None
