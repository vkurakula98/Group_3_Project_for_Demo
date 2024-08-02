from flask import Blueprint, render_template, request, flash
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
  return render_template("RegistrationConfirm.html")

@views.route('/faq')
def faq():
  return render_template("FAQ.html")

