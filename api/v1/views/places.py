#!/usr/bin/python3
"""
Restful Place
"""
from flask import Flask, jsonify, abort, request, make_response
from models.place import Place
from models.city import City
from models.user import User
import json
from api.v1.views import app_views
from models import storage
import hashlib


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieve all places linked to a city_id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def a_place(place_id):
    """Retrieve one place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """remove a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """new place"""
    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    if 'user_id' not in response:
        abort(400, "Missing user_id")
    if "name" not in response:
        abort(400, "Missing name")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user_id = response['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    response['city_id'] = city_id
    place = Place(**response)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place info"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")

    for key, value in response.items():
        if key not in ["id", "user_id", "created_at", "updated_at", "city_id"]:
            setattr(place, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
