import sqlalchemy as db
from flask import Flask
from os import  path

DB_NAME = "database.db"


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'p@SSWORD'
    app.config['SQLALCHEMY_DATABASE_URI'] = db.create_engine(f'sqlite:///{DB_NAME}')

    # mongo = pymongo(app)
    from .views import views
    # from .auth import auth

    app.register_blueprint(views, name=__name__, url_prefix='/')
    # app.register_blueprint(auth, name=__name__, url_prefix='/')

    from .models import Student

    # create_database(app)

    return app

# def create_database(app):
#     if not path.exists('Website/'+DB_NAME):
#         # db.create_engine(app=app)
#         # print('Created Database')


