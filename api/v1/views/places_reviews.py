#!/usr/bin/python3
"""
Manipulating Reviews objects in database storage.
"""
import json
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('places/<place_id>/reviews', strict_slashes=False)
def get_reviews_by_place(place_id):
    """ Retrieve all reviews linked to a place from then database """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in storage.all(Review).values():
        if review.place_id == place.id:
            reviews.append(review)
    place_reviews = [review.to_dict() for review in reviews]

    output = jsonify(place_reviews)
    output.data = json.dumps(place_reviews, indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('reviews/<review_id>', strict_slashes=False)
def get_review_by_id(review_id):
    """ Retrieve a specific review from the database """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    output = jsonify(review.to_dict())
    output.data = json.dumps(review.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a review from the database if found """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a new revie object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'text' not in data:
        abort(400, description='Missing text')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    review = Review(**data)
    review.place_id = place_id
    review.save()
    review_data = storage.get(Review, review.id)
    output = jsonify(review.to_dict())
    output.data = json.dumps(review_data.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 201


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Update a Review object by ID """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    output = jsonify(review.to_dict())
    output.data = json.dumps(review.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 200
