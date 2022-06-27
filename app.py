import os
from flask import Flask, jsonify, redirect
from dotenv import load_dotenv
from database import connect_db
from models import Student

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']
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

connect_db(app)