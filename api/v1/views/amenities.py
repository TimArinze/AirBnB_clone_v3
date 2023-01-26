#!/usr/bin/python3
"""
creating route
"""
from api.v1.views import app_views
import json
from flask import jsonify, Flask, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """get all amenities"""
    all_amenities = storage.all(Amenity)
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """get a particular amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/ameniteies/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a particular amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    del amenity
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """get a particular amenity"""
    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    if "name" not in response:
        abort(400, "Missing name")
    new_amenity = Amenity(**response)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update a particular amenity name"""
    response = request.get_json()
    if not response:
        abort(400, "not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    attributes = ["id", "created_at", "updated_at"]
    for key, value in response.items():
        if key not in attributes:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
