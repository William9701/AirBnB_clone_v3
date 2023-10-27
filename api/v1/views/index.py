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
