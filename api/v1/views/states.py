#!/usr/bin/python3
"""
Manipulating state objects in storage.
"""
import json
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_states():
    """ Retrieve all state objects from the database """
    from models import storage
    from models.state import State
    all_states = storage.all(State)
    states_list = [state.to_dict() for state in all_states.values()]

    output = jsonify(states_list)
    output.data = json.dumps(states_list, indent=2) + '\n'
    output.content_type = 'application/json'
    return output

@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state_by_id(state_id):
    """ Retrieve all state objects from the database """
    from models import storage
    from models.state import State
    state = storage.get(State, state_id)
    if state is None:
        error = {"error": "Not found"}
        output = jsonify(error)
        output.data = json.dumps(error, indent=2) + '\n'
        output.content_type = 'application/json'
        return output
    output = jsonify(state.to_dict())
    output.data = json.dumps(state.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output
