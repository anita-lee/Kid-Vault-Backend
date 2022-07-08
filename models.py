from database import db

class Student(db.Model):
    """ Student model """

    __tablename__ = 'students'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    birth_date = db.Column(
        db.Date,
        nullable=False
    )

    classroom = db.Column(
        db.String(50),
        nullable=True
    )

    @classmethod
    def get_by_id(cls, id):
        """ Get student by id """

        return cls.query.filter_by(id=id).first()

    def serialize(self):
        """ Serialize student """

        return {
            'id': self.id,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'birth_date': self.birth_date,
            'classroom': self.classroom
        }

class Contact(db.Model):
    """ Contact model """

    __tablename__ = 'contacts'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
    )

    name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=True
    )

    phone = db.Column(
        db.String(50),
        nullable=True
    )

    other = db.Column(
        db.String(50),
        nullable=True
    )

    relation = db.Column(
        db.String(50),
        nullable=True
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    def serialize(self):
        """ Serialize contact """

        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'other': self.other,
            'relation': self.relation
        }

class MedicalRecord(db.Model):
    """ Medical record model """

    __tablename__ = 'medical_records'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
        primary_key=True
    )

    student_weight = db.Column(
        db.Float,
        nullable=True
    )

    student_height = db.Column(
        db.Float,
        nullable=True
    )

    polio = db.Column(
        db.Date,
        nullable=True
    )

    mmr = db.Column(
        db.Date,
        nullable=True
    )

    covid1 = db.Column(
        db.Date,
        nullable=True
    )

    covid2 = db.Column(
        db.Date,
        nullable=True
    )

    flu = db.Column(
        db.Date,
        nullable=True
    )

    tb = db.Column(
        db.Date,
        nullable=True
    )

    tetanus = db.Column(
        db.Date,
        nullable=True
    )

    def serialize(self):
        """ Serialize medical record """

        return {
            'student_id': self.student_id,
            'student_weight': self.student_weight,
            'student_height': self.student_height,
            'polio': self.polio,
            'mmr': self.mmr,
            'covid1': self.covid1,
            'covid2': self.covid2,
            'flu': self.flu,
            'tb': self.tb,
            'tetanus': self.tetanus
        }

class User(db.Model):
    """ User model """

    __tablename__ = 'users'

    username = db.Column(
        db.String(50),
        primary_key=True
    )

    password = db.Column(
        db.String(50),
        nullable=False
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False
    )

    phone = db.Column(
        db.String(50),
        nullable=False
    )

    is_guardian = db.Column(
        db.String,
        nullable=False
    )

    def serialize(self):
        """ Serialize user """

        return {
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'is_guardian': self.is_guardian
        }


class GuardianChild(db.Model):
    """ GuardianChild model """

    __tablename__ = 'guardian_children'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    username = db.Column(
        db.String(50),
        db.ForeignKey('users.username')
    )

    child_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id')
    )

    child = db.relationship(
        'Student',
        backref=db.backref('guardian_children', lazy=True)
    )

    user = db.relationship(
        'User',
        backref=db.backref('guardian_children', lazy=True)
    )

    def serialize(self):
        """ Serialize guardian child """

        return {
            'guardian_username': self.guardian_username,
            'child_id': self.child_id
        }