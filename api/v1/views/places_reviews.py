#!/usr/bin/python3

"""
   States module
   View for State objects that handles all default RestFul API actions
"""
from models.review import Review
from models.place import Place
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_place_reviews(place_id=None):
    """ Retrieves all the reviews of a place with a given id """

    if place_id is None:
        return abort(404)
    my_place = storage.get(Place, place_id)
    if my_place is None:
        return abort(404)

    reviews = my_place.reviews
    out = [review.to_dict() for review in reviews]
    return jsonify(out)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_a_review(review_id=None):
    """ Retrieves a review object according to its id """

    if review_id is None:
        return abort(404)
    my_review = storage.get(Review, review_id)
    if my_review is not None:
        my_review = my_review.to_dict()
        return jsonify(my_review)

    return abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_review(review_id=None):
    """ Deletes a Review object according to its id """

    if review_id is None:
        return abort(404)
    my_review = storage.get(Review, review_id)
    if my_review is not None:
        storage.delete(my_review)
        storage.save()
        return make_response(jsonify({}), 200)

    return abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_a_review(place_id=None):
    """
        Creates a new Review object according to
        the HTTP body request dictionary
    """
    if place_id is None:
        return abort(404)

    my_place = storage.get(Place, place_id)
    if my_place is None:
        return abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if "user_id" not in body:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user_id = body['user_id']
    my_user = storage.get(User, user_id)
    if my_user is None:
        return abort(404)

    if "text" not in body:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    new = Review(**body)
    new.place_id = place_id
    storage.save()
    return make_response(jsonify(new.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_a_review(review_id=None):
    """ Updates a review object according to its id """

    to_ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    if review_id is None:
        return abort(404)

    my_review = storage.get(Review, review_id)

    if my_review is not None:
        body = request.get_json(silent=True)
        if body is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)

        for key, value in body.items():
            if key not in to_ignore:
                setattr(my_review, key, value)
        my_review.save()

        return make_response(jsonify(my_review.to_dict()), 200)

    return abort(404)
