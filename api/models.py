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
    __tablename__ = 'personal_information'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id', ondelete='CASCADE'), unique=True)
    first_name = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    last_name = db.Column(db.VARCHAR(1000), default=None, nullable=True)
    

    def __init__(self, first_name, last_name, user_id):
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id

    def to_dict(self):
        return {
            "First Name": self.first_name,
            "Last Name": self.last_name,
        }

class StudentInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    grade_level = db.Column(db.Enum(EducationLevel), default=None, nullable=True)
    subjects = db.Column(ARRAY(db.Integer), nullable=False, default=list)

    def __init__(self, user_id, grade_level, subjects):
        self.user_id = user_id
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

    def __init__(self, user_id, subjects, experience, attempted_education, completed_education, training_complete = False):
        self.user_id = user_id
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

    """
    The availability columns will be a JSON object with the following structure:
        [<start_time>, <end_time>]

    """
    mon_avail = db.Column(JSON, nullable=True) 
    tue_avail = db.Column(JSON, nullable=True)
    wed_avail = db.Column(JSON, nullable=True)
    thurs_avail = db.Column(JSON, nullable=True)
    fri_avail = db.Column(JSON, nullable=True)
    sat_avail = db.Column(JSON, nullable=True)
    sun_avail = db.Column(JSON, nullable=True)

    vacation_days = db.Column(JSON, nullable=False) #A list of the days a tutor is unavailable to work [day1, day2, ..., dayk] in YYYY-MM-DD

    def __init__(self, user_id, mon, tue, wed, thurs, fri, sat, sun, vacation_days):
        self.user_id = user_id
        self.mon_avail = mon
        self.tue_avail = tue
        self.wed_avail = wed
        self.thurs_avail = thurs
        self.fri_avail = fri
        self.sat_avail = sat
        self.sun_avail = sun
        self.vacation_days = vacation_days

        now = datetime.now()
        self.month = str(now.year) + "-" + str(now.month)

    def to_dict(self):
        return{
            "Month": self.month,
            "Availability": self.availability
        }
    
class Messaging(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    sender_id = db.Column(db.String(36), default=None, nullable=False)
    receiver_id = db.Column(db.String(36), default=None, nullable=False)
    message = db.Column(db.Text, default=None, nullable=False)
    time_sent = db.Column(db.DateTime, nullable=False)

    def __init__(self, sender_id, receiver_id, message, time_sent):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.message = message
        self.time_sent = datetime.utcnow()



        
