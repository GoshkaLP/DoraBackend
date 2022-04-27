from os import getenv

# Для отладки
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET = getenv('JWT_SECRET')
PASSWORD_SALT = getenv('PASSWORD_SALT')
BASE_URL = getenv('BASE_URL')
