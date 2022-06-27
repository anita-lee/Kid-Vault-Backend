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
        nullable=False
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

class Vaccination(db.Model):
    """ Vaccination model """

    __tablename__ = 'vaccinations'

    student_id = db.Column(
        db.Integer,
        db.ForeignKey('students.id'),
    )
    polio = db.Column(
        db.Date,
        nullable=True
    )

    mmr = db.Column(
        db.Date,
        nullable=True
    )

    covid = db.Column(
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

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )


