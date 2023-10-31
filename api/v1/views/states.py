#!/usr/bin/python3
"""
Manipulating state objects in storage.
"""
import json
from flask import jsonify, abort, request
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
        abort(404)
    output = jsonify(state.to_dict())
    output.data = json.dumps(state.to_dict(), indent=2) + '\n'
    output.content_type = 'application/json'
    return output


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Deletes the state instance from the dict"""
    from models import storage
    from models.state import State
    from models.city import City
    from models.place import Place
    from models.review import Review
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ a method that creates a state obj"""
    from models.state import State

    if not request.get_json():
        abort(400, description='Not a JSON')

    body = request.get_json()
    if 'name' not in body:
        abort(400, description='Missing name')

    state = State(**body)
    state.save()
    output = jsonify(state.to_dict())
    output.data = json.dumps(state.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ update a state class"""
    from models import storage
    from models.state import State
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    dont_update = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in dont_update:
            setattr(state, key, value)
    state.save()
    output = jsonify(state.to_dict())
    output.data = json.dumps(state.to_dict(), indent=2) + '\n'
    output.content_type = "application/json"
    return output, 200
