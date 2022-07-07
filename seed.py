from app import app
from database import db
from csv import DictReader
from models import Student
from models import Contact
from models import MedicalRecord
from models import GuardianChild
from models import User

db.drop_all(app=app)
db.cascade_drop = True
db.create_all(app=app)

with open('csv/students.csv') as students:
    db.session.bulk_insert_mappings(Student, DictReader(students))

with open('csv/contacts.csv') as contacts:
    db.session.bulk_insert_mappings(Contact, DictReader(contacts))

with open('csv/medical_records.csv') as medical_records:
    db.session.bulk_insert_mappings(MedicalRecord, DictReader(medical_records))

with open('csv/guardian_children.csv') as guardian_children:
    db.session.bulk_insert_mappings(GuardianChild, DictReader(guardian_children))

with open('csv/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

db.session.commit()