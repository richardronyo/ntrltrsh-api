from flask import Blueprint

signup_route = Blueprint('signup', __name__)

from api.routes.signup import routes