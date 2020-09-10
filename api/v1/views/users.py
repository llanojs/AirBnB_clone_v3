#!/usr/bin/python3

"""
   Users module
   View for Users objects that handles all default RestFul API actions
"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves all the users stored """
    users = storage.all(User)
    out = [user.to_dict() for user in users.values()]
    return jsonify(out)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_a_user(user_id=None):
    """ Retrieves a user object according to its id """

    if user_id is None:
        return abort(404)
    my_user = storage.get(User, user_id)
    if my_user is not None:
        my_user = my_user.to_dict()
        return jsonify(my_user)

    return abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_user(user_id=None):
    """ Deletes a user object according to its id """

    if user_id is None:
        return abort(404)
    my_user = storage.get(User, user_id)
    if my_user is not None:
        storage.delete(my_user)
        storage.save()
        return make_response(jsonify({}), 200)

    return abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_a_user():
    """
        Creates a new User object according to
        the HTTP body request dictionary
    """
    body = request.get_json(silent=True)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "email" not in body:
        return make_response(jsonify({'error': 'Missing email'}), 400)

    if "password" not in body:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new = User(**body)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_a_user(user_id=None):
    """ Updates a user object according to its id """
    if user_id is None:
        return abort(404)

    my_user = storage.get(User, user_id)

    if my_user is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(my_user, key, value)
        my_user.save()
        return make_response(jsonify(my_user.to_dict()), 200)
    return abort(404)
