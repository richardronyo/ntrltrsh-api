from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config.update(
    DEBUG=True,
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:cmpt395!@ntrltrsh-db.postgres.database.azure.com:5432/postgres?",
    SQLALCHEMY_TRACK_MODIFICATIONS=True
)

db = SQLAlchemy(app)
jwt = JWTManager(app)

from api import models

@jwt.user_lookup_loader
def user_loader_callback(jwt_header, jwt_data):
    user_id = jwt_data["sub"]  # `sub` represents the `identity` used in create_access_token(identity=user_id)
    user = models.LoginInformation.query.filter(models.LoginInformation.id == user_id).one_or_none()

    return user# Modify as necessary to fetch the user by ID

with app.app_context():
    db.create_all()
    db.session.commit()

