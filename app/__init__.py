from flask import Flask
from flask_cors import CORS
from config import Config
from app.middleware.auth import jwt_required
from app.routes import api_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    return app