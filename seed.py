from app import app
from database import db
from csv import DictReader
from models import Student
from models import Contact
from models import Vaccination

db.drop_all(app=app)
db.create_all(app=app)

with open('csv/students.csv') as students:
    db.session.bulk_insert_mappings(Student, DictReader(students))

with open('csv/contacts.csv') as contacts:
    db.session.bulk_insert_mappings(Contact, DictReader(contacts))

with open('csv/vaccinations.csv') as vaccinations:
    db.session.bulk_insert_mappings(Vaccination, DictReader(vaccinations))

db.session.commit()