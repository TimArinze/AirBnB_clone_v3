#!/usr/bin/python3
"""
State objects
"""
from api.v1.views import app_views
import json
from flask import jsonify, make_response, request
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states')
def all_states():
    """retrieves all states"""
    response = storage.all(State)
    return jsonify([obj.to_dict() for obj in response.values()])


@app_views.route('/states/<state_id>')
def state_object(state_id):
    """retrieve state using id"""
    new_list = []
    response = storage.all(State)
    for obj in response.values():
        dictionary = obj.to_dict()
        if dictionary["id"] == state_id:
            new_list.append(dictionary)
    return jsonify(new_list)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes States Object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    del state
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'])
def create_state():
    try:
        data = request.get_json()
    except:
        return make_response("Not a JSON", 400)
    if "name" not in data:
        return make_response("Missing name", 400)
    new_state = {"name": data["name"]}
    return make_response(jsonify(new_state), 201)
