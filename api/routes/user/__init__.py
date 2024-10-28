from flask import Blueprint

user_route = Blueprint('user', __name__)

from api.routes.user import routes