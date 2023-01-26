#!/usr/bin/python3
"""
creating route
"""
from api.v1.views import app_views
import json
from flask import jsonify, Flask, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """get all cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get a particular city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete a particular city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    del city
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """get a particular city"""
    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    if "name" not in response:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    response["state_id"] = state_id
    new_city = City(**response)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update a particular city name"""
    response = request.get_json()
    if not response:
        abort(400, "not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    attributes = ["id", "state_id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in attributes:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
