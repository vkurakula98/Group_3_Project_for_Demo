
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'p@SSWORD'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    # from .auth import auth

    app.register_blueprint(views, name=__name__, url_prefix='/')
    # app.register_blueprint(auth, name=__name__, url_prefix='/')

    from .models import Student,Coordinator

    with app.app_context():
        db.create_all()

    create_database(app)

    return app

def create_database(app):
    if not path.exists(f'Website/{DB_NAME}'):
        with app.app_context():
          db.create_all()
        #db.create_all(app=app)
        print('Created Database')



