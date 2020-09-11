#!/usr/bin/python3

"""
   States module
   View for State objects that handles all default RestFul API actions
"""
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_place_amenities(place_id):
    """ Retrieves all the amenities of a place with a given id """

    if place_id is None:
        return abort(404)
    my_place = storage.get(Place, place_id)
    if my_place is None:
        return abort(404)

    amenities = my_place.amenities
    out = [review.to_dict() for review in amenities]
    return jsonify(out)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_a_place_amenity(place_id=None, amenity_id=None):
    """ Removes a object according to its id """

    if place_id is None or amenity_id is None:
        return abort(404)

    my_place = storage.get(Place, place_id)
    if my_place is None:
        return abort(404)

    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        return abort(404)

    if my_amenity not in my_place.amenities:
        return abort(404)

    my_place.amenities.remove(my_amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_an_amenity(place_id=None, amenity_id=None):
    """
        Links an Amenity object to a place according to
        their respective id
    """

    if place_id is None or amenity_id is None:
        return abort(404)

    my_place = storage.get(Place, place_id)
    if my_place is None:
        return abort(404)

    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        return abort(404)

    if my_amenity in my_place.amenities:
        return make_response(jsonify(my_amenity.to_dict()), 200)

    my_place.amenities.append(my_amenity)
    storage.save()

    return make_response(jsonify(my_amenity.to_dict()), 201)
