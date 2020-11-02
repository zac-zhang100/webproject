from flask import Flask
from config import Config
from flask_login import LoginManager


login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # from app.api import bp as api_bp
    # app.register_blueprint(api_bp,url_prefix='/api')
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

#from app import routes
