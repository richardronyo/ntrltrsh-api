from api.routes.admin import admin_route

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from api.lib.admin.admin_funcs import retrieve_all_users, clear_database, change_account_type

@admin_route.route('/all_users', methods=["GET"])
def get_all_users():
    return jsonify(retrieve_all_users()), 200

@admin_route.route('/clear_database', methods = ["DELETE"])
def del_users():
    return jsonify(clear_database()), 200

@admin_route.route('change_account', methods = ["PUT"])
@jwt_required()
def change():
    user_id = current_user.id
    return jsonify(change_account_type(user_id)), 200