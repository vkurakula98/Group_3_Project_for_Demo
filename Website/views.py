from flask import Blueprint, render_template, request, flash, jsonify

from Website.models import User

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

@views.route('Register')
def RegCnf():
    data = request.get_json()
    role = data.get('role')
    user_id = data.get('user_id')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    dob = data.get('dob')
    department = data.get('department')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return jsonify({'msg': 'Passwords do not match'}), 400

    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({'msg': 'User already exists'}), 400

    User.register_user(role, user_id, first_name, last_name, dob, department, email, password)
    return jsonify({'msg': 'User registered successfully'}), 201

@views.route('/faq')
def faq():
  return render_template("FAQ.html")

