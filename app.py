import os
from flask import Flask, jsonify, redirect, request
from dotenv import load_dotenv
from database import connect_db, db
from models import Student, Contact, MedicalRecord, User, GuardianChild

load_dotenv()

database_url = os.environ['DATABASE_URL']

# fix incorrect database URIs currently returned by Heroku's pg setup
database_url = database_url.replace('postgres://', 'postgresql://')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

@app.get("/")
def homepage():
    """Show home."""

    return redirect("/students")

@app.get("/students")
def get_students():
    """Get all students."""

    students = Student.query.all()
    return jsonify([student.serialize() for student in students])

@app.get("/students/<int:id>")
def get_student(id):
    """Get student by id."""

    student = Student.query.get(id)
    return jsonify(student.serialize())

@app.get("/contacts")
def get_contacts():
    """Get all contacts."""

    contacts = Contact.query.all()
    return jsonify([contact.serialize() for contact in contacts])

@app.get("/medicalrecords")
def get_medicalrecords():
    """Get all medical records."""

    medical_records = MedicalRecord.query.all()
    return jsonify([medical_record.serialize() for medical_record in medical_records])

@app.get("/users")
def get_users():
    """Get all users."""

    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.get("/guardianchildren")
def get_guardianchildren():
    """Get all guardian children. """

    guardian_children = GuardianChild.query.all()
    return jsonify([guardian_child.serialize() for guardian_child in guardian_children])

@app.post("/students")
def create_student():
    """Create a new student."""

    student = Student(
        last_name=request.json['last_name'],
        first_name=request.json['first_name'],
        birth_date=request.json['birth_date'],
        classroom=request.json['classroom']
    )
    
    db.session.add(student)
    db.session.commit()
    return jsonify(student.serialize())

@app.post("/guardianchildren")
def create_guardianchild():
    """Create a new guardian child relationship."""

    guardian_child = GuardianChild(
       guardian_username=request.json['guardian_username'],
       child_id=request.json['child_id']
    )

    db.session.add(guardian_child)
    db.session.commit()
    return jsonify(guardian_child.serialize())

@app.post("/users")
def create_user():
    """Create a new user."""

    user = User(
        username=request.json['username'],
        password=request.json['password'],
        first_name=request.json['first_name'],
        last_name=request.json['last_name'],
        email=request.json['email'],
        phone=request.json['phone'],
        is_guardian=request.json['is_guardian']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

connect_db(app)