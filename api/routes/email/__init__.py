from flask import Blueprint

email_route = Blueprint('email', __name__)

from api.routes.email import routes