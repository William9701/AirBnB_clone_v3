#!/usr/bin/python3
""" This module returns the city obj """
import json
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def view_cities_by_states(state_id):
    """ lists cities under a particular state"""
    from models.city import City
    from models import storage
    from models.state import State

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_list = []
    all_cities = storage.all(City).values()

    for cities in all_cities:
        if cities.state_id == state_id:
            city_list.append(cities.to_dict())

    output = jsonify(city_list)
    output.data = json.dumps(city_list, indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 200


@app_views.route('/cities/<city_id>', strict_slashes=False)
def view_cities(city_id):
    """ view the city object"""
    from models.city import City
    from models import storage

    cities = storage.get(City, city_id)
    if not cities:
        abort(404)
    else:
        output = jsonify(cities.to_dict())
        output.data = json.dumps(cities.to_dict(), indent=2) + '\n'
        output.content_type = 'application/json'
        return output, 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city using its id"""
    from models.city import City
    from models import storage
    from models.place import Place
    from models.review import Review

    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        places = storage.all(Place).values()
        for place in places:
            if place.city_id == city.id:
                # Get all Review objects related to this Place
                reviews = storage.all(Review).values()
                # Delete all Review objects related to this Place
                for review in reviews:
                    if review.place_id == place.id:
                        storage.delete(review)
                # Now we can safely delete the Place
                storage.delete(place)
        # Now we can safely delete the City
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ a method that creates a city obj"""
    from models import storage
    from models.state import State
    from models.city import City

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(404, 'Not a JSON')

    body = request.get_json()
    if 'name' not in body:
        abort(400, 'Missing name')

    city = City(**body)
    city.state_id = state_id
    city.save()
    output = jsonify(city.to_dict())
    output.data = json.dumps(city.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ update a city instance"""
    from models import storage
    from models.city import City
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    data = request.get_json()
    dont_update = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in dont_update:
            setattr(city, key, value)
    storage.save()
    output = jsonify(city.to_dict())
    output.data = json.dumps(city.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 200
