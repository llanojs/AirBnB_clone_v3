#!/usr/bin/python3

"""
   Cities module
   View for City objects that handles all default RestFul API actions
"""
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_places(city_id=None):
    """ Retrieves all the place stored """
    if city_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    my_city = storage.get(City, city_id)
    if my_city is not None:
        place_list = [place.to_dict() for place in my_city.places]
        return jsonify(place_list)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_a_place(place_id=None):
    """Retrieves a place according to its id"""
    if place_id is None:
        return make_response(jsonify({'error': 'No found'}), 404)
    my_place = storage.get(Place, place_id)
    if my_place is not None:
        return jsonify(my_place.to_dict())
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_place(place_id=None):
    """Delete a place according to its id"""
    if place_id is None:
        return abort(404)
    my_place = storage.get(Place, place_id)
    if my_place is not None:
        storage.delete(my_place)
        storage.save()
        return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_a_place(city_id=None):
    """
        Create a place associate to its city_id, according
        to HTTP body request dictionary
    """
    if city_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    body = request.get_json(silent=True)
    city = storage.get(City, city_id)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "user_id" not in body:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if "name" not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    user = storage.get(User, body['user_id'])
    if city and user:
        body['city_id'] = city_id
        new = Place(**body)
        new.save()
        return make_response(jsonify(new.to_dict()), 201)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_a_place(place_id=None):
    """ Updates a place object according to ids id """
    if place_id is None:
        return abort(404)

    my_place = storage.get(Place, place_id)

    if my_place is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, value in body.items():
            if key not in ['id', 'created_at',
                           'user_id', 'city_id', 'updated_at']:
                setattr(my_place, key, value)
        my_place.save()

        return make_response(jsonify(my_place.to_dict()), 200)
    return abort(404)
