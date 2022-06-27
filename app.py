import os
from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from database import connect_db
from models import Student, Contact, Vaccination

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

@app.get("/vaccinations")
def get_vaccinations():
    """Get all vaccinations."""

    vaccinations = Vaccination.query.all()
    return jsonify([vaccination.serialize() for vaccination in vaccinations])

connect_db(app)