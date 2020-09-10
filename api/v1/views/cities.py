#!/usr/bin/python3

"""
   Cities module
   View for City objects that handles all default RestFul API actions
"""
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/states/<state_id>/cities/', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(state_id=None):
    """ Retrieves all the cities stored """
    if state_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    my_state = storage.get(State, state_id)
    if my_state is not None:
        city_list = my_state.cities
        city_list = [city.to_dict() for city in city_list]
        return jsonify(city_list)
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_a_city(city_id=None):
    """Retrieves a city according to its id"""
    if city_id is None:
        return make_response(jsonify({'error': 'No found'}), 404)
    my_city = storage.get(City, city_id)
    if my_city is not None:
        my_city = my_city.to_dict()
        return jsonify(my_city)
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_a_city(city_id=None):
    """Delete a city according to its id"""
    if city_id is None:
        return abort(404)
    my_city = storage.get(City, city_id)
    if my_city is not None:
        storage.delete(my_city)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_a_city(state_id=None):
    """
        Create a city associate to its state_id, according
        to HTTP body request dictionary
    """
    if state_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    body = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    if state_id and state:
        body['state_id'] = state_id
        new = City(**body)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)
    return abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_a_city(city_id=None):
    """ Updates a city object according to ids id """
    if city_id is None:
        return abort(404)

    my_city = storage.get(City, city_id)

    if my_city is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(my_city, key, value)
        my_city.save()

        return make_response(jsonify(my_city.to_dict()), 200)
    return abort(404)
