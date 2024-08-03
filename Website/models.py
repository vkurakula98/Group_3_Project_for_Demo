from flask_pymongo import PyMongo
from flask import Flask
import bcrypt

app = Flask(__name__)
app.config.from_object('config.Config')
mongo = PyMongo(app)


class User:
    @staticmethod
    def register_user(role, user_id, first_name, last_name, dob, department, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        mongo.db.users.insert_one({
            'role': role,
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'department': department,
            'email': email,
            'password': hashed_password
        })

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({'email': email})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
