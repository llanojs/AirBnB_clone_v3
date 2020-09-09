#!/usr/bin/python3

"""
   States module
   View for State objects that handles all default RestFul API actions
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves all the amenities stored """
    amenities = storage.all(Amenity)
    out = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(out)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_an_amenity(amenity_id=None):
    """ Retrieves an amenity object according to its id """

    if amenity_id is None:
        return abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is not None:
        my_amenity = my_amenity.to_dict()
        return jsonify(my_amenity)

    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_an_amenity(amenity_id=None):
    """ Deletes a Amenity object according to its id """

    if amenity_id is None:
        return abort(404)
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is not None:
        storage.delete(my_amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_a_amenity():
    """
        Creates a new Amenity object according to
        the HTTP body request dictionary
    """
    body = request.get_json(silent=True)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "name" not in body:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    new = Amenity(**body)
    new.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_an_amenity(amenity_id=None):
    """ Updates a amenity object according to its id """

    if amenity_id is None:
        return abort(404)

    my_amenity = storage.get(Amenity, amenity_id)

    if my_amenity is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, value in body.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(my_amenity, key, value)
        my_amenity.save()

        return make_response(jsonify(my_amenity.to_dict()), 200)

    return abort(404)
