from . import db
from flask_login import UserMixin
#from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
import datetime


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to track events a student has registered for
    registered_events = db.relationship('Event', secondary='registration', back_populates='registered_students')


class Coordinator(db.Model):
    coordinator_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to allow a coordinator to create multiple events
    events = db.relationship('Event', backref='coordinator', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    time_period = db.Column(db.String(10), nullable=False)
    event_time = db.Column(db.Time, nullable=False)
    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.coordinator_id'), nullable=False)

    # Relationship to track students registered for this event
    registered_students = db.relationship('Student', secondary='registration', back_populates='registered_events')


# Association Table for the many-to-many relationship between Event and Student
registration = db.Table('registration',
                        db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True),
                        db.Column('student_id', db.Integer, db.ForeignKey('student.student_id'), primary_key=True)
                        )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    answer_text = db.Column(db.Text)
    asked_on = db.Column(db.DateTime, default=db.func.now())
    answered_on = db.Column(db.DateTime)

    student_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('questions', lazy=True))

    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.coordinator_id'))
    coordinator = db.relationship('Coordinator', backref=db.backref('answers', lazy=True))



