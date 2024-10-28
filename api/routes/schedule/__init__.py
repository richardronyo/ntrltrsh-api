from flask import Blueprint

schedule_route = Blueprint('schedule', __name__)

from api.routes.schedule import routes