import enum
import uuid

from flask import Blueprint
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSON

from api import db

class AccountType(enum.Enum):
    ADMIN = 0
    TUTOR = 1
    STUDENT = 2

class EducationLevel(enum.Enum):
    ELEMENTARY = 1
    JUNIOR_HIGH = 2
    HIGH_SCHOOL = 3
    UNIVERSITY = 4

class Subject(enum.Enum):
    MATHEMATICS = 1
    ENGLISH = 2
    SCIENCE = 3
    BIOLOGY = 4
    CHEMISTRY = 5
    PHYSICS = 6

class Experience(enum.Enum):
    ZERO = 0
    ONE = 1
    TWO_TO_FOUR = 2
    FIVE_TO_TEN = 3
    TEN_PLUS = 4

class LoginInformation(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    username = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    password = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    account_type = db.Column(db.Enum(AccountType), default=AccountType.STUDENT, nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, username, password, account_type):
        self.email = email
        self.username = username
        self.password = password
        self.account_type = account_type
        self.date_created = datetime.utcnow()

    def to_dict(self):
        return {
            'Email': self.email,
            'Username': self.username,
            'Password': self.password,
            'Account Type': self.account_type.name,
            'Date Created': self.date_created.isoformat()
        }

class PersonalInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    first_name = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    last_name = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    date_of_birth = db.Column(db.DateTime(), default=None, nullable=True)

    def __init__(self, first_name, last_name, date_of_birth, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.user_id = user_id


    def to_dict(self):
        return {
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Date of Birth": self.date_of_birth.strftime('%A, %B %d, %Y')
        }

class StudentInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    grade_level = db.Column(db.Enum(EducationLevel), default=None, nullable=True)
    subjects = db.Column(ARRAY(db.Integer), nullable=False, default=list)

    def __init__(self, grade_level, subjects):
        self.grade_level = grade_level
        self.subjects = subjects

    def to_dict(self):
        return {
            "Grade Level": self.grade_level.name,
            "Subjects": [Subject(subject).name for subject in self.subjects]
        }

class TutorInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    subjects = db.Column(ARRAY(db.Integer), nullable=False, default=list)
    experience = db.Column(db.Enum(Experience), default=None, nullable=True)
    attempted_education = db.Column(db.VARCHAR(1000), default=None, nullable=False)
    completed_education = db.Column(db.Boolean, default=True, nullable=False)
    training_complete = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, subjects, experience, attempted_education, completed_education, training_complete = False):
        self.subjects = subjects
        self.experience = experience
        self.attempted_education = attempted_education
        self.completed_education = completed_education
        self.training_complete = training_complete

    def to_dict(self):
        return {
            "Subjects": [Subject(subject).name for subject in self.subjects],
            "Years of Experience": self.experience,
            "Highest Attempted Education Level": self.attempted_education,
            f"Completed {self.attempted_education}": self.completed_education,
            "Completed Onboarding Training": self.training_complete
        }

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    month = db.Column(db.String, nullable=False) #ie. 2024-09
    availability = db.Column(JSON, nullable=False)

    def __init__(self, month, availaibility):
        self.month = month
        self.availability = availaibility

    def to_dict(self):
        return{
            "Month": self.month,
            "Availability": self.availability
        }

        
