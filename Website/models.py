import db
from sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from main import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)