#!/usr/bin/python3
""" This is a palce_amenities api module"""
import json
from flask import jsonify, abort, request

import models
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def amenities_of_place(place_id):
    """ Returns the amenities of a place"""
    from models.place import Place
    from models import storage

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if models.storage_t == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids

    amenities_list = [amenity.to_dict() for amenity in amenities]

    output = jsonify(amenities_list)
    output.data = json.dumps(amenities_list, indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """ deletes the amenity obj"""
    from models.place import Place
    from models import storage
    from models.amenity import Amenity

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    # Check if the amenity is linked to the place
    if models.storage_t == 'db':
        if amenity not in place.amenities:
            abort(404)
        else:
            storage.delete(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        else:
            storage.delete(amenity_id)

    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def link_amenity(place_id, amenity_id):
    """ Links an amenity obj to a place"""
    from models.place import Place
    from models import storage
    from models.amenity import Amenity

    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    # Check if the amenity is already linked to the place
    if models.storage_t == 'db':
        if amenity in place.amenities:
            output = jsonify(amenity.to_dict())
            output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
            output.content_type = 'application/json'
            return output, 200
        else:
            place.amenities = amenity
    else:
        if amenity_id in place.amenity_ids:
            output = jsonify(amenity.to_dict())
            output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
            output.content_type = 'application/json'
            return output, 200
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    output = jsonify(amenity.to_dict())
    output.data = json.dumps(amenity.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output, 201
