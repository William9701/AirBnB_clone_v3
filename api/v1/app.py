#!/usr/bin/python3
""" This is a setup module """
import json

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    error = {"error": "Not found"}
    output = jsonify(error)
    output.data = json.dumps(error, indent=2) + "\n"
    output.content_type = "application/json"
    output.status_code = 404
    return output


if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        host = os.environ["HBNB_API_HOST"]
    else:
        host = "0.0.0.0"

    if "HBNB_API_PORT" in os.environ:
        port = os.environ["HBNB_API_PORT"]
    else:
        port = "5000"

    app.run(host=host, port=port, threaded=True)
