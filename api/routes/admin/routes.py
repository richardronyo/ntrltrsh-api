from api.routes.admin import admin_route

from flask import request, jsonify

from api.lib.admin.admin_funcs import retrieve_all_users, clear_users

@admin_route.route('/all_users', methods=["GET"])
def get_all_users():
    return jsonify(retrieve_all_users()), 200

@admin_route.route('/clear_users', methods = ["DELETE"])
def del_users():
    return jsonify(clear_users()), 200

