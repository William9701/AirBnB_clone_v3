#!/usr/bin/python3
"""
Manipulating user objects in database storage.
"""
import json
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', strict_slashes=False)
def get_users():
    """ Retrieve all user objects from the database """
    all_users = storage.all(User)
    users_list = [user.to_dict() for user in all_users.values()]

    output = jsonify(users_list)
    output.data = json.dumps(users_list, indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('users/<user_id>', strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieve a specific user from the database """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    output = jsonify(user.to_dict())
    output.data = json.dumps(user.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user object from the database if found """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create a new user object """
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'email' not in data:
        abort(400, description='Missing email')
    if 'password' not in data:
        abort(400, description='Missing password')
    user = User(**data)
    user.save()
    user_data = storage.get(User, user.id)
    output = jsonify(user_data.to_dict())
    output.data = json.dumps(user_data.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 201


@app_views.route('users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ Update a User object by ID """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    output = jsonify(user.to_dict())
    output.data = json.dumps(user.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 200
