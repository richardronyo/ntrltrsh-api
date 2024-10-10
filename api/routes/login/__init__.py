from flask import Blueprint

login_route = Blueprint('login', __name__)

from api.routes.login import routes