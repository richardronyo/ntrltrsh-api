from api.routes.login import login_route

from flask import request, jsonify

from api.lib.login.login_funcs import login_verification

@login_route.route('/', methods=["POST"])
def login():
    user = request.get_json()

    return jsonify(login_verification(user)), 200