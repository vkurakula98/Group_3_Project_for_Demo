

import bcrypt
import encodings

from . import db
import mongo
from flask import Blueprint, render_template, request, flash, jsonify, url_for, request, session, redirect, url_for
from .models import Student
from werkzeug.security import generate_password_hash, check_password_hash
# from Website.models import User

views = Blueprint('views',__name__)

@views.route('/')
def home():
    #return "<h1>Test</h1>"
    return render_template("Base.html")
@views.route('/login')
def login():
  return render_template("choice.html")

@views.route('/coordinator_login')
def login_student():
  return render_template("Login_Coordinator.html")

@views.route('/student_login')
def login_coordinator():
  return render_template("Login_Student.html")

@views.route('/home')
def base():
  return render_template("Base.html")

@views.route('/signup')
def signup():
  return render_template("Signup.html")

@views.route('/submit_signup',methods=['POST','GET'])
def RegCnf():
    # data = request.form
    # print(data)
    if request.method == 'POST':
        role = request.form.get('Select Role')
        Student_ID = request.form.get('Student ID')
        First_Name = request.form.get('First Name')
        Last_Name = request.form.get('Last Name')
        DoB = request.form.get('Date of Birth')
        Department = request.form.get('Department')
        email_id = request.form.get('Email ID')
        password = request.form.get('Password')
        if role == 'Student':
            new_user = Student(Student_ID=Student_ID,email_id=email_id,First_Name=First_Name,Last_Name=Last_Name,DoB=DoB,Department=Department,password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('views.home'))
        #elif role == 'Coordinator':


        password = request.form.get('Password')
        CnfPassword = request.form.get('Confirm Password')

        # if len(email) < 4:
        #     pass
        # elif password != CnfPassword:
        #     pass


    return render_template("RegistrationConfirmed.html")

@views.route('/faq')
def faq():
  return render_template("FAQ.html")

