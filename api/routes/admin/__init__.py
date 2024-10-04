from flask import Blueprint

admin_route = Blueprint('admin', __name__)

from api.routes.admin import routes