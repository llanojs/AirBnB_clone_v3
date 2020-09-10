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


@app_views.route('/states/<state_id>/cities/', methods=['GET'], strict_slashes=False)
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
    """Retrieves a city acording the id"""
    if city_id is None:
        return make_response(jsonify({'error': 'No found'}), 404)
    my_city = storage.get(City, city_id)
    if my_city is not None:
        my_city = my_city.to_dict()
        return jsonify(my_city)
    return abort(404)

