#!/usr/bin/python3
"""
State objects
"""
from api.v1.views import app_views
import json
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.base_model import BaseModel
from models.state import State


@app_views.route('/states/')
@app_views.route('/states')
def all_states():
    """retrieves all states"""
    response = storage.all(State)
    return jsonify([obj.to_dict() for obj in response.values()])


@app_views.route('/states/<state_id>', strict_slashes=False)
def state_object(state_id):
    """retrieve state using id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes States Object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    del state
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """create state object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """put state object"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    attributes = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in attributes:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
