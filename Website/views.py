import datetime

import Website.models
from . import db
from flask import Blueprint, render_template, request, flash, jsonify, url_for, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Student, Coordinator, Event, registration, Question
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views',__name__)
#Page navigation
@views.route('/home')
def base():
  return render_template("Base.html")
@views.route('/signup')
def signup():
  return render_template("Signup.html")
@views.route('/')
def home():
    #return "<h1>Test</h1>"
    return render_template("Base.html")
@views.route('/login')
def login():
    return render_template("login.html")
@views.route('/faq')
def faq():
  return render_template("FAQ.html")
@views.route('/events')
def events():
  return render_template("Events.html")
@views.route('/departments')
def departments():
  return render_template("Departments.html")
@views.route('/about')
def About():
  return render_template("About.html")
@views.route('/contact')
def Contact():
  return render_template("Contact.html")



#Authorisation
@views.route('/submit_login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']

        user = None
        if role == 'student':
            user = Student.query.filter_by(email=email).first()
        elif role == 'coordinator':
            user = Coordinator.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            session['role'] = role
            flash('Login successful!', 'success')
            if role == 'student':
                session['user_id'] = user.student_id
                session[role] = {
                    'student_id': user.student_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
                session.permanent = True
                return redirect(url_for('Website.student_profile'))
            elif role == 'coordinator':
                session['user_id'] = user.coordinator_id
                session[role] = {
                    'coordinator_id': user.coordinator_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                }
                session.permanent = True
                return redirect(url_for('Website.coordinator_profile'))

        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')
@views.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        role = request.form['role']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        dob = datetime.datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        department = request.form['department']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if role == 'student':
            student_id = request.form['student-id']
            # Check if email already exists in Student table
            if Student.query.filter_by(email=email).first():
                flash('Email is already registered as a student!', 'danger')
                return render_template('signup.html')
                # Check if email student_id exists in Student table
            if Student.query.filter_by(student_id=student_id).first():
                flash('student_id is already registered as a student!', 'danger')
                return render_template('signup.html')
            new_user = Student(student_id=student_id, first_name=first_name, last_name=last_name, dob=dob, department=department, email=email, password=hashed_password)
        elif role == 'coordinator':
            coordinator_id = request.form['coordinator-id']
            # Check if email already exists in Coordinator table
            if Coordinator.query.filter_by(email=email).first():
                flash('Email is already registered as a coordinator!', 'danger')
                return render_template('signup.html')
                # Check if email student_id exists in Student table
            if Coordinator.query.filter_by(coordinator_id=coordinator_id).first():
                flash('student_id is already registered as a student!', 'danger')
                return render_template('signup.html')
            new_user = Coordinator(coordinator_id=coordinator_id, first_name=first_name, last_name=last_name, dob=dob, department=department, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        #return redirect(url_for('Website.RegistrationConfirmed'))
        #return render_template("RegistrationConfirmed.html")
        return render_template("RegistrationConfirmed.html")
    return render_template("signup.htm")

#changes made by viswanath
@views.route('/student_profile')
def student_profile():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    student = Student.query.get(session['user_id'])
    return render_template('student_profile.html', student=student)

# @views.route('/coordinator_profile')
# def coordinator_profile():
#     if 'user_id' not in session or session['role'] != 'coordinator':
#         return redirect(url_for('views.login'))
#
#     coordinator = Coordinator.query.get(session['user_id'])
#     return render_template('coordinator_profile.html')
@views.route('/coordinator_profile')
def coordinator_profile():
    if 'user_id' not in session or session['role'] != 'coordinator':
        return redirect(url_for('views.login'))

    # Fetch the coordinator details from the database
    coordinator = Coordinator.query.get(session['user_id'])

    if coordinator is None:
        # Handle the case where the coordinator is not found
        return redirect(url_for('views.login'))

    # Pass the coordinator object to the template
    return render_template('coordinator_profile.html', coordinator=coordinator)


@views.route('/')

@views.route('/Coordinator_home')
def home_return_coordinator():
    return redirect(url_for('Website.coordinator_profile'))

@views.route('/Student_home')
def home_return_student():
    return redirect(url_for('Website.student_profile'))
@views.route('/event_creation')
def event_creation():
    coordinator = session.get('coordinator')
    return render_template('Event_creation_form.html', coordinator=coordinator)
@views.route('/create_event', methods=['GET', 'POST'])
def event_creation_submission():
    coordinator = session.get('coordinator')

    if not coordinator:
        return redirect('/login')  # Redirect to login if not logged in

    if request.method == 'POST':
        # Retrieve form data
        event_name = request.form['event_name']
        description = request.form['description']
        # event_date = request.form['event-date']
        location = request.form['location']
        time_period = request.form['time_period']
        # event_time = request.form['Event Time']
        event_time = datetime.datetime.strptime(request.form['event_time'], '%H:%M').time()
        #image = request.files['image']
        event_date = datetime.datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()

        # Store event in the database
        new_event = Event(
            event_name=event_name,
            description=description,
            event_date=event_date,
            location=location,
            time_period=time_period,
            event_time=event_time,
            coordinator_id=coordinator['coordinator_id']  # Use coordinator ID from session
        )

        db.session.add(new_event)
        db.session.commit()

        #return redirect('Event_creation_form.html')  # Redirect or render a success template
        events = Event.query.filter_by(coordinator_id=coordinator['coordinator_id']).all()
        return render_template('Event_creation_form.html', coordinator=coordinator, events=events)
        # return render_template('Event_creation_form.html', coordinator=coordinator)

    return render_template('Event_creation_form.html', coordinator=coordinator)
@views.route('/view_events')
def event_creation_view():
    coordinator = session.get('coordinator')
    events = Event.query.filter_by(coordinator_id=coordinator['coordinator_id']).all()
    return render_template('Created_Events_view.html', coordinator=coordinator, events=events)
@views.route('/view_questions')
def view_questions():
    coordinator = session.get('coordinator')
    student = session.get('student')

    coordinator_id = session.get('coordinator_id')
    student = session.get('student_id')

    return render_template('answer_questions.html', student=student, coordinator=coordinator)

# changes made in registration form

@views.route('/ask_questions')
def ask_questions():
    coordinator = session.get('coordinator')
    student = session.get('student')

    coordinator_id = session.get('coordinator_id')

    return render_template('ask_question.html', student=student, coordinator=coordinator)
@views.route('/viewing_events')
def event_viewing_view():
    student = session.get('student')
    print("student:", student)

    if student is None:
        return redirect('/login')  # Redirect to login if the student is not logged in

    # Get the department of the student
    student_id = student.get('student_id')
    if not student_id:
        return "Student ID not found in session", 400

    student_info = Student.query.filter_by(student_id=student_id).first()
    if student_info is None:
        return "Student not found", 404

    department = student_info.department

    # Find coordinators in the same department
    coordinators = Coordinator.query.filter_by(department=department).all()
    coordinator_ids = [coordinator.coordinator_id for coordinator in coordinators]
    print("coor:", coordinator_ids)

    # Find events created by these coordinators
    events = Event.query.filter(Event.coordinator_id.in_(coordinator_ids)).all()
    print("events:", events)

    return render_template('View_events_students.html', student=student, events=events)
@views.route('/edit_event/<int:event_id>', methods=['GET'])
def edit_event(event_id):
    coordinator = session.get('coordinator')
    event = Event.query.get_or_404(event_id)

    return render_template('edit_event.html', event =event, coordinator = coordinator)


@views.route('/update_event/<int:event_id>', methods=['POST'])
def update_event(event_id):
    coordinator = session.get('coordinator')
    event = Event.query.get_or_404(event_id)
    event.event_name = request.form['event_name']
    event.description = request.form['description']
    # event.event_date = request.form['event_date']
    # event.event_time = request.form['event_time']
    event.location = request.form['location']
    event.time_period = request.form['time_period']
    event.event_time = datetime.datetime.strptime(request.form['event_time'], '%H:%M:%S').time()
    event.event_date = datetime.datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()

    db.session.commit()
    # return redirect(url_for('Website.Created_Events_view'),event = event, coordinator = coordinator)
    events = Event.query.filter_by(coordinator_id=coordinator['coordinator_id']).all()
    return render_template('Created_Events_view.html',events = events, coordinator = coordinator)
@views.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    events = db.session.query(Event).filter_by(id=event_id).all()
    print("event_id:", event_id)
    print("events:", events)
    # event = Event.query.get_or_404(event_id).all()
    if len(events) is 1:
        print("going to delete")
        db.session.delete(events[0])
        db.session.commit()
    else:
        print("returning 404")
        return "Some issue", 404
    coordinator = session.get('coordinator')
    return render_template('Created_Events_view.html', coordinator=coordinator, events=events)


@views.route('/register_event/<int:event_id>', methods=['POST'])
def register_event(event_id):
    student = session.get('student')
    if not student:
        flash('Please log in to register for events.', 'danger')
        return redirect(url_for('login_page'))

    student_id = student['student_id']

    # Check if the student is already registered for the event
    registrations = db.session.query(registration).filter_by(student_id=student_id, event_id=event_id).first()

    if registrations:
        flash('You are already registered for this event.', 'info')
    else:
        # Register the student for the event
        stmt = registration.insert().values(event_id=event_id, student_id=student_id)
        db.session.execute(stmt)
        db.session.commit()
        flash('Successfully registered for the event!', 'success')

    return jsonify({'status': 'registered'})
@views.route('/unregister_event/<int:event_id>', methods=['POST'])
def unregister_event(event_id):
    student = session.get('student')
    if not student:
        flash('Please log in to unregister from events.', 'danger')
        return redirect(url_for('login_page'))

    student_id = student['student_id']

    # Check if the student is registered for the event
    registrations = db.session.query(registration).filter_by(student_id=student_id, event_id=event_id).first()

    if registrations:
        # Unregister the student from the event
        stmt = registration.delete().where(registration.c.event_id == event_id).where(
            registration.c.student_id == student_id)
        db.session.execute(stmt)
        db.session.commit()
        flash('Successfully unregistered from the event!', 'success')

    return jsonify({'status': 'unregistered'})

@views.route('/get_registered_students/<int:event_id>')
def get_registered_students(event_id):
    # Fetch students registered for the event
    registered_students = db.session.query(Student.student_id, Student.first_name, Student.last_name).join(registration).filter(registration.c.event_id == event_id).all()

    students = [{'student_id': student.student_id, 'first_name': student.first_name, 'last_name': student.last_name} for student in registered_students]

    return jsonify({'students': students})

@views.route('/remove_student/<int:event_id>/<int:student_id>', methods=['POST'])
def remove_student(event_id, student_id):
    student = session.get('student')
    if not student:
        flash('Please log in to unregister from events.', 'danger')
        return redirect(url_for('login_page'))

    # Check if the student is registered for the event
    registrations = db.session.query(registration).filter_by(student_id=student_id, event_id=event_id).first()

    if registrations:
        # Unregister the student from the event
        stmt = registration.delete().where(registration.c.event_id == event_id).where(
            registration.c.student_id == student_id)
        db.session.execute(stmt)
        db.session.commit()
        flash('Successfully unregistered from the event!', 'success')

    return jsonify({'status': 'unregistered'})

@views.route('/logout')
def logout():
    # Remove user session data
    session.pop('user_id', None)
    session.pop('user_role', None)
    # Redirect to login or home page
    return redirect(url_for('Website.login'))

# @views.route('/')
# def index():
#     if 'coordinator_id' in session:
#         return redirect(url_for('coordinator_profile'))
#     return redirect(url_for('login'))


# question and answer

@views.route('/submit_question', methods=['POST'])
def submit_question():
    data = request.get_json()
    question_text = data.get('question')

    if not question_text:
        return jsonify({'success': False, 'error': 'No question provided'}), 400

    student_id = request.args.get('student_id')  # Assuming student_id is passed as a query parameter

    # Find the student object
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'success': False, 'error': 'Student not found'}), 404

    # Create a new question entry
    new_question = Question(
        question_text=question_text,
        student_id=student.id
    )

    try:
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@views.route('/answer_questions')
def answer_questions(event_id):
    student_id = session.get('student_id')
    coordinator_id = session.get('coordinator_id')  # assuming session stores logged-in coordinator's ID
    coordinator = Coordinator.query.get_or_404(coordinator_id)
    student = Student.query.get_or_404(student_id)
    # students_in_same_department = Student.query.filter_by(department=coordinator.department).all()
    questions = db.session.query(Question).filter_by(student.department==coordinator.department).first()
    # questions = Question.query.filter_by(coordinator_id=None, student.has(department=coordinator.department)).all()
    return render_template('answer_questions.html', questions=questions)


@views.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data['question_id']
    answer_text = data['answer_text']

    question = Question.query.get_or_404(question_id)
    question.answer_text = answer_text
    question.answered_on = datetime.now()
    question.coordinator_id = session.get('coordinator_id')  # set the answering coordinator

    db.session.commit()
    return jsonify({'success': True})

