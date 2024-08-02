from flask import Flask

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'p@SSWORD'

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, name=__name__, url_prefix='/')
    # app.register_blueprint(auth, name=__name__, url_prefix='/')

    return app





