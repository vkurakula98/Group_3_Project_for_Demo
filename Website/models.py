from . import db
from flask_login import UserMixin
#from sqlalchemy.sql import func
class Student(db.Model, UserMixin):
    Student_ID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True)
    password = db.column(db.String(150))
    first_name = db.column(db.String(150))
    last_name = db.column(db.String(150))
    Date_Of_Birth = db.column(db.DateTime(timezone=True))
    Department = db.column(db.String(150))
    # Time_of_Registration = db.column(db.DateTime(timezone=True), default=func.now())


