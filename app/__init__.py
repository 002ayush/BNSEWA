from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .config import Config

mongo = PyMongo()  # MongoDB instance
bcrypt = Bcrypt()  # Bcrypt instance for password hashing
jwt = JWTManager()  # JWT instance for token management

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from Config class

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register routes
    from .routes import routes
    app.register_blueprint(routes)

    return app
