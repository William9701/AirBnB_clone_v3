#!/usr/bin/python3
""" This module returns the amenities obj """
import json
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """ list all the amenities instances"""
    from models import storage
    from models.amenity import Amenity

    amenities = storage.all(Amenity)
    amenities_list = [amenities.to_dict() for amenities in amenities.values()]

    output = jsonify(amenities_list)
    output.data = json.dumps(amenities_list, indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_by_id(amenity_id):
    """ Lists the amenities by id"""
    from models import storage
    from models.amenity import Amenity

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        output = jsonify(amenity.to_dict())
        output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
        output.content_type = 'application/json'
        return output


@app_views.route('/amenities/<amenity_id>', strict_slashes=False, methods=[
    'DELETE'])
def delete_amenity(amenity_id):
    """ this deletes the amenity obj"""
    from models import storage
    from models.amenity import Amenity

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """ a method that creates a state obj"""
    from models.amenity import Amenity

    if not request.get_json():
        abort(400, description='Not a JSON')

    body = request.get_json()
    if 'name' not in body:
        abort(400, description='Missing name')

    amenity = Amenity(**body)
    amenity.save()
    output = jsonify(amenity.to_dict())
    output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ update a amenity class"""
    from models import storage
    from models.amenity import Amenity
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    data = request.get_json()
    dont_update = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in dont_update:
            setattr(amenity, key, value)
    storage.save()
    output = jsonify(amenity.to_dict())
    output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 200
