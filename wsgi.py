from app import create_app

from config import DevConfig, ProdConfig

# Не забыть поменять на ProdConfig
app = create_app(ProdConfig)

if app is None:
    print('[Error]: No config provided')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
