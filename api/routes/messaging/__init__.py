from flask import Blueprint

messaging_route = Blueprint("messaging", __name__)

from api.routes.messaging import routes