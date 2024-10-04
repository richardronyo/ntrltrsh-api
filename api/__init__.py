from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:cmpt395!@ntrltrsh-db.postgres.database.azure.com:5432/postgres?",
    SQLALCHEMY_TRACK_MODIFICATIONS=True
)

db = SQLAlchemy(app)

from api import models

with app.app_context():
    db.create_all()
    db.session.commit()

