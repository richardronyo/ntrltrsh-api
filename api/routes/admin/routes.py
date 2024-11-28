from api.routes.admin import admin_route

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user

from api.lib.admin.admin_funcs import retrieve_all_users, clear_database, change_account_type, create_admin, clear_schedule_and_shifts

@admin_route.route('/all_users', methods=["GET"])
def get_all_users():
    return jsonify(retrieve_all_users()), 200

@admin_route.route('/clear_database', methods = ["DELETE"])
def del_users():
    return jsonify(clear_database()), 200

@admin_route.route('/change_account', methods = ["PUT"])
@jwt_required()
def change():
    user_id = current_user.id
    return jsonify(change_account_type(user_id)), 200

@admin_route.route('/create_admin', methods = ["POST"])
def create():
    return jsonify(create_admin()), 200

@admin_route.route('/clear_schedule', methods = ["DELETE"])
def clear_schedule():
    return jsonify(clear_schedule_and_shifts()), 200