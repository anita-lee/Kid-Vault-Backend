import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import User, db, connect_db, Student, MedicalRecord,DEFAULT_PROFILE_PIC, GuardianChild, Contact
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
# from forms import CSRFTokenForm

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['CORS_HEADERS'] = ['Content-Type','Authorization']
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

jwt = JWTManager(app)
toolbar = DebugToolbarExtension(app)


connect_db(app)

# ##############################################################################
# # CSRF Protection:

# # @app.before_request
# # def add_csrf_only_form():
# #     """Add a CSRF-only form so that every route can use it"""

# #     g.csrf_form = CSRFProtection()


##############################################################################
# JWT Protection:


@jwt.user_identity_loader
def user_identity_lookup(user):
    """ Register a callback fn that takes whatever obj that is passed in
        as the identity when creating JWTs and converts it to a JSON
        serializable format """

    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """ Register a callback function that loads a user from your database
        whenever a protected route is accessed. This should return any python
        object on a successful lookup, or None if the lookup failed for any
        reason (for example if the user has been deleted from the database)."""

    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


##############################################################################
# User Signup and Login:

@app.post('/signup')
@cross_origin()
def signup():
    """Handle user signup.
    Create new user and add to DB. Return Token.
    If the there already is a user with that username: return False
    """
    try:
        user = User.signup(
            username=request.json["username"],
            password=request.json["password"],
            first_name=request.json["first_name"],
            last_name=request.json["last_name"],
            email=request.json["email"],
            phone=request.json["phone"],
        )

        db.session.commit()

    except IntegrityError:
        return (jsonify({"error": "Duplicate Username/Email"}), 400)

    if user.username:
        token = create_access_token(identity=user.username)
        return (jsonify(token=token), 201)


@app.post('/login')
@cross_origin()
def login():
    """ Handle user login and return a token """

    user = User.login(
        username=request.json["username"],
        password=request.json["password"]
    )

    if user:
        token = create_access_token(identity=user.username)
        return (jsonify(token=token), 200)

    else:
        return (jsonify({"error": "Invalid Username/Password"}), 400)

##############################################################################
# General User routes:


@app.get("/users")
@cross_origin()
def get_users():
    """Get all users."""

    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.patch('/users/<username>')
@cross_origin()
@jwt_required()

def update_user(username):
    """Update a user's current info."""

    curr_user = get_jwt_identity()

    if curr_user == username:

        user = User.query.get_or_404(username)
        user.first_name = request.json.get('first_name', user.first_name)
        user.last_name = request.json.get('last_name', user.last_name)
        user.email = request.json.get('email', user.email)
        user.phone = request.json.get('phone', user.phone)

        db.session.commit()
        return (jsonify({"success": "user updated!"}), 200)

    else:
        return (jsonify({"error": "Unauthorized."}), 401)

##############################################################################
# General Student routes:


@app.get("/")
@cross_origin()
def homepage():
    """Show students."""

    return redirect("/students")


@app.get("/students")
@cross_origin()
def get_students():
    """Get all students."""

    students = Student.query.all()
    return jsonify([student.serialize() for student in students])


@app.get("/students/<int:id>")
@cross_origin()
def get_student(id):
    """Get student by id."""

    student = Student.query.get(id)
    return jsonify(student.serialize())

@app.post('/students')
@cross_origin()
def create_student():
    """Create a new student."""

    try:
        student = Student.add(
            last_name=request.json['last_name'],
            first_name=request.json['first_name'],
            birth_date=request.json['birth_date'],
            classroom=request.json['classroom'],
            image_url=request.json['image_url']
        )

        db.session.commit()
        return (jsonify({"success" : "Student added. "}), 200)

    except IntegrityError:
        return (jsonify({"error": "Duplicate Student"}), 400)

@app.delete('/students/<int:id>')
@cross_origin()
def delete_student(id):
    """Delete a student."""

    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return (jsonify({"success" : "Student deleted."}), 200)

##############################################################################
# General Contacts routes:


@app.get("/contacts")
@cross_origin()
def get_contacts():
    """Get all contacts."""

    contacts = Contact.query.all()
    return jsonify([contact.serialize() for contact in contacts])


@app.get("/contacts/<int:student_id>")
@cross_origin()
def get_contact(student_id):
    """Get contacts by student id."""

    contacts = Contact.get_by_id(student_id)
    print("****************contact: ", contacts)
    return jsonify([contact.serialize() for contact in contacts])


##############################################################################
# General Medical Record routes:


@app.get("/medicalrecords")
@cross_origin()
def get_medicalrecords():
    """Get all medical records."""

    medical_records = MedicalRecord.query.all()
    return jsonify([medical_record.serialize() for medical_record in medical_records])


@app.get("/medicalrecords/<int:student_id>")
@cross_origin()
def get_medicalrecord(student_id):
    """Get medical records by student id."""

    medical_record = MedicalRecord.query.get(student_id)
    return jsonify(medical_record.serialize())


##############################################################################
# General GuardianChildren Record routes:


@app.get("/guardianchildren")
@cross_origin()
def get_guardianchildren():
    """Get all guardian children. """

    guardian_children = GuardianChild.query.all()
    return jsonify([guardian_child.serialize() for guardian_child in guardian_children])


@app.get("/guardianchildren/<guardian_username>")
@cross_origin()
def get_guardianchild(guardian_username):
    """Get guardian children by guardian ."""

    guardian_children = GuardianChild.get_by_guardian(guardian_username)
    print("****************guardian_children: ", guardian_children)
    return jsonify([guardian_child.serialize() for guardian_child in guardian_children])


@app.post("/guardianchildren")
@cross_origin()
def create_guardianchild():
    """Create a new guardian child relationship."""

    guardian_child = GuardianChild(
       guardian_username=request.json['guardian_username'],
       child_id=request.json['child_id']
    )

    db.session.add(guardian_child)
    db.session.commit()
    return jsonify(guardian_child.serialize())