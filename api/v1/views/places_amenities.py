#!/usr/bin/python3
"""
Restful Place
"""
from flask import Flask, jsonify, abort, request, make_response
from models.place import Place
from models.review import Review
from models.user import User
import json
from api.v1.views import app_views
from models import storage
import hashlib


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities(place_id):
    """Retrieve all amenities linked to a place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(place_id, amenity_id):
    """remove a amenity linked to a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if place.id != amenity.place_id:
        abort(404)
        storage.delete(amenity)        
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity(place_id, amenity_id):
    """new amenity"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if place.id == amenity.place_id:
        return jsonify(amenity.to_dict()), 200
    amenity['place_id'] = place_id
    review = Review(**amenity)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
