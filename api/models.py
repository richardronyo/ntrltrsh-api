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
    UNSPECIFIED = 0
    ELEMENTARY = 1
    JUNIOR_HIGH = 2
    HIGH_SCHOOL = 3
    UNIVERSITY = 4

class Math(enum.Enum):
    
    ALGEBRA = 1
    CALCULUS = 2
    GEOMETRY = 3
    TRIGONOMETRY = 4
    STATISTICS = 5
    PROBABILITY = 6
    DIFFERENTIAL_EQUATIONS = 7
    LINEAR_ALGEBRA = 8
    GENERAL_MATH = 9

class Science(enum.Enum):
    PHYSICS = 1
    CHEMISTRY = 2
    BIOLOGY = 3
    EARTH_SCIENCE = 4
    ASTRONOMY = 5
    ENVIRONMENTAL_SCIENCE = 6
    BOTANY = 7
    ZOOLOGY = 8
    GENERAL_SCIENCE = 9


class Language(enum.Enum):
    FRENCH = 1
    SPANISH = 2
    GERMAN = 3
    CHINESE = 4
    JAPANESE = 5
    RUSSIAN = 6
    ITALIAN = 7
    ARABIC = 8

class English(enum.Enum):
    LITERATURE = 1
    GRAMMAR = 2
    WRITING = 3
    POETRY = 4
    DRAMA = 5
    ESSAY_WRITING = 6
    CRITICAL_ANALYSIS = 7
    CREATIVE_WRITING = 8
    GENERAL_ENGLISH = 9

class History(enum.Enum):
    ANCIENT = 1
    MEDIEVAL = 2
    MODERN = 3
    WORLD_WAR_I = 4
    WORLD_WAR_II = 5
    AMERICAN_REVOLUTION = 6
    INDUSTRIAL_REVOLUTION = 7
    COLD_WAR = 8
    SOCIAL_STUDIES = 9


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
    registration_complete = db.Column(db.Boolean, default = False, nullable = True)
    date_complete = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, email, username, password, account_type):
        self.email = email
        self.username = username
        self.password = password
        self.account_type = account_type
        self.date_created = datetime.utcnow()
        self.registration_complete = False

    def to_dict(self):
        return {
            'Email': self.email,
            'Username': self.username,
            'Password': self.password,
            'Account Type': self.account_type.name,
            'Date Created': self.date_created.isoformat(),
            "Registration Status": "Complete" if self.registration_complete else "Incomplete",
            "Date Complete": self.date_complete.isoformat() if self.registration_complete else "Incomplete"
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
    math = db.Column(ARRAY(db.Enum(Math)), nullable=True)
    science = db.Column(ARRAY(db.Enum(Science)), nullable=True)
    language = db.Column(ARRAY(db.Enum(Language)), nullable=True)
    english = db.Column(ARRAY(db.Enum(English)), nullable=True)
    history = db.Column(ARRAY(db.Enum(History)), nullable=True)
    profile_headline = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)

    def __init__(self, user_id, grade_level, math, science, language, english, history):
        self.user_id = user_id
        self.grade_level = grade_level
        self.math = math
        self.science = science
        self.language = language
        self.english = english
        self.history = history

    def to_dict(self):
        return {
            "Grade Level": self.grade_level.name if self.grade_level else None,
            "Math": [subject.name for subject in self.math] if self.math else [],
            "Science": [subject.name for subject in self.science] if self.science else [],
            "Language": [subject.name for subject in self.language] if self.language else [],
            "English": [subject.name for subject in self.english] if self.english else [],
            "History": [subject.name for subject in self.history] if self.history else []
        }

class TutorInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    math = db.Column(ARRAY(db.Enum(Math)), nullable=True)
    science = db.Column(ARRAY(db.Enum(Science)), nullable=True)
    language = db.Column(ARRAY(db.Enum(Language)), nullable=True)
    english = db.Column(ARRAY(db.Enum(English)), nullable=True)
    history = db.Column(ARRAY(db.Enum(History)), nullable=True)
    experience = db.Column(db.Enum(Experience), default=None, nullable=True)
    undergrad_college = db.Column(db.VARCHAR(1000), default = None, nullable = True)
    undergrad_major = db.Column(db.VARCHAR(1000), default = None, nullable = True)
    graduate_college = db.Column(ARRAY(db.VARCHAR(1000)), default = None, nullable = True)
    graduate_major = db.Column(ARRAY(db.VARCHAR(1000)), default = None, nullable = True)
    teaching_certification = db.Column(db.VARCHAR(1000), default = None, nullable = True)
    profile_headline = db.Column(db.String, nullable = True)
    bio = db.Column(db.String, nullable = True)

    def __init__(self, user_id, math, science, language, english, history):
        self.user_id = user_id
        self.math = math
        self.science = science
        self.language = language
        self.english = english
        self.history = history

    def to_dict(self):
        return {
            "Math": [subject.name for subject in self.math] if self.math else [],
            "Science": [subject.name for subject in self.science] if self.science else [],
            "Language": [subject.name for subject in self.language] if self.language else [],
            "English": [subject.name for subject in self.english] if self.english else [],
            "History": [subject.name for subject in self.history] if self.history else [],
            "Undergraduate Studies": self.undergrad_college,
            "Graduate Studies": self.graduate_college,
            "Teaching Certification": self.teaching_certification
        }

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('login_information.id'), unique=True)
    schedule_type = db.Column(db.Enum(AccountType), default=AccountType.TUTOR, nullable=False)
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



    def __init__(self, user_id, account_type, mon, tue, wed, thurs, fri, sat, sun, vacation_days):
        self.user_id = user_id
        self.schedule_type = account_type
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
            "MONDAY": self.mon_avail,
            "TUESDAY": self.tue_avail,
            "WEDNESDAY": self.wed_avail,
            "THURSDAY": self.thurs_avail,
            "FRIDAY": self.fri_avail,
            "SATURDAY": self.sat_avail,
            "SUNDAY": self.sun_avail,
            "VACATION": self.vacation_days
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

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    student_id = db.Column(db.String(36), default=None, nullable=False)
    tutor_id = db.Column(db.String(36), default=None, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    day = db.Column(db.VARCHAR(1000), default=None, nullable=False)
    day_generated = db.Column(db.DateTime, nullable=False)

    start_time = db.Column(db.VARCHAR(1000), nullable=False)
    end_time = db.Column(db.VARCHAR(1000), nullable=False)

    def __init__(self, student_id, tutor_id, date, start_time, end_time):
        self.student_id = student_id
        self.tutor_id = tutor_id
        self.date = date
        self.day = date.weekday()
        self.day_generated = datetime.utcnow()
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return{
            "STUDENT_ID": self.student_id,
            "TUTOR_ID": self.tutor_id,
            "DATE": self.date,
            "DAY": self.day,
            "START_TIME": self.start_time,
            "END_TIME": self.end_time
        }

class Bugs(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    reporter_id = db.Column(db.String(36), default=None, nullable=False)
    title = db.Column(db.VARCHAR(1000), default = None, nullable = False)
    description = db.Column(db.VARCHAR(10000), default = None, nullable = False)
    time_submitted = db.Column(db.DateTime, nullable=False)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, reporter_id, title, description):
        self.reporter_id = reporter_id
        self.title = title
        self.description = description
        self.time_submitted = datetime.utcnow()

        return
        
    def to_dict(self):
        return {
            "Bug ID": self.id,
            "Reporter ID": self.reporter_id,
            "Title": self.title,
            "Description": self.description,
            "Time Submitted": self.time_submitted,
            "Bug Reviewed": self.reviewed
        }

class Shifts(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    tutor_id = db.Column(db.String(36), default = None, nullable = False)
    start_day = db.Column(db.VARCHAR(1000), default = None, nullable = False)
    end_day = db.Column(db.VARCHAR(1000), default = None, nullable = False)
    num_of_shifts = db.Column(db.Integer, default = 0, nullable = True)

    def __init__(self, tutor_id, start_day, end_day, num_of_shifts = 1):
        self.tutor_id = tutor_id
        self.start_day = start_day
        self.end_day = end_day
        self.num_of_shifts = num_of_shifts

    def add_shift(self):
        self.num_of_shifts += 1

    

        

        
