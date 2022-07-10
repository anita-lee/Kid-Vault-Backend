import os
from flask import Flask, jsonify, request, redirect
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import User, db, connect_db, Student, MedicalRecord,DEFAULT_PROFILE_PIC, GuardianChild, Contact
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

app.config['CORS_HEADERS'] = ['Content-Type','Authorization']
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']
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



##### USER SIGN UP AND LOGIN #####

@app.route('/signup', methods=["POST"])
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


# import os
# from flask import Flask, jsonify, redirect, request, session, g
# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
# from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError
# from dotenv import load_dotenv
# from database import connect_db, db
# from models import Student, Contact, MedicalRecord, User, GuardianChild
# from datetime import timedelta
# # from forms import CSRFProtection
# # from flask_cors import CORS, cross_origin

# load_dotenv()

# app = Flask(__name__)

# app.config["JWT_TOKEN_LOCATION"] = ["headers"]
# app.config["JWT_COOKIE_SECURE"] = False
# app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY']
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     os.environ['DATABASE_URL'].replace('postgres://', 'postgresql://'))
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = False
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# jwt = JWTManager(app)
# toolbar = DebugToolbarExtension(app)

# connect_db(app)


# ##############################################################################
# # User signup/login/logout

# # @app.before_request
# # def add_csrf_only_form():
# #     """Add a CSRF-only form so that every route can use it"""

# #     g.csrf_form = CSRFProtection()


##############################################################################
# General user routes:


@app.get("/")
@cross_origin()
def homepage():
    """Show home."""

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

@app.get("/contacts")
@cross_origin()
def get_contacts():
    """Get all contacts."""

    contacts = Contact.query.all()
    return jsonify([contact.serialize() for contact in contacts])

@app.get("/medicalrecords")
@cross_origin()
def get_medicalrecords():
    """Get all medical records."""

    medical_records = MedicalRecord.query.all()
    return jsonify([medical_record.serialize() for medical_record in medical_records])

@app.get("/users")
@cross_origin()
def get_users():
    """Get all users."""

    users = User.query.all()
    return jsonify([user.serialize() for user in users])

@app.get("/guardianchildren")
@cross_origin()
def get_guardianchildren():
    """Get all guardian children. """

    guardian_children = GuardianChild.query.all()
    return jsonify([guardian_child.serialize() for guardian_child in guardian_children])

@app.post("/students")
@cross_origin()
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

@app.post("/users")
@cross_origin()
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