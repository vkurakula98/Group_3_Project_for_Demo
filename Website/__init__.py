from flask import Flask
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_jwt_secret')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/flask_auth')

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'p@SSWORD'

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, name=__name__, url_prefix='/')
    # app.register_blueprint(auth, name=__name__, url_prefix='/')

    return app





