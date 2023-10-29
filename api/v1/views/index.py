import json

from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def index():
    """ returns a status ok"""
    data = {"status": "OK"}
    response = jsonify(data)
    response.data = json.dumps(data, indent=2) + "\n"
    response.content_type = 'application/json'
    return response


@app_views.route('/stats')
def stats():
    """ Retrieving the count of objects in databse """
    from models import storage

    stats = {}
    name_map = {'State': 'states', 'User': 'users',
                'Amenity': 'amenities', 'Review': 'reviews',
                'Place': 'places', 'City': 'cities'
                }
    classes_to_count = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    for cls in classes_to_count:
        count = storage.count(cls)
        mapped_name = name_map.get(cls, cls)
        stats[mapped_name] = count
    output = jsonify(stats)
    output.data = json.dumps(stats, indent=2) + "\n"
    output.content_type = 'application/json'
    return output
