#!/usr/bin/python3
"""
Manipulating Place objects in database storage.
"""
import json
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """ Retrieve all places linked to a city from then database """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city.id:
            places.append(place)
    city_places = [place.to_dict() for place in places]

    output = jsonify(city_places)
    output.data = json.dumps(city_places, indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('places/<place_id>', strict_slashes=False)
def get_place_by_id(place_id):
    """ Retrieve a specific place from the database """
    place = storage.get(User, place_id)
    if place is None:
        abort(404)
    output = jsonify(place.to_dict())
    output.data = json.dumps(place.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a place from the database if found """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create a new place object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description='Missing user_id')
    if 'name' not in data:
        abort(400, description='Missing name')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    place = Place(**data)
    place.city_id = city_id
    place.save()
    place_data = storage.get(Place, place.id)
    output = jsonify(place_data.to_dict())
    output.data = json.dumps(place_data.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a Place object by ID """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    output = jsonify(place.to_dict())
    output.data = json.dumps(place.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 200
