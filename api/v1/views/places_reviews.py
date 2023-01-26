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


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieve all review linked to a place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def a_review(review_id):
    """Retrieve one review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """remove a review"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """new review"""
    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    if 'user_id' not in response:
        abort(400, "Missing user_id")
    if "text" not in response:
        abort(400, "Missing text")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    user_id = response['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    response['place_id'] = place_id
    review = Review(**response)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review info"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")

    attributes = ["id", "user_id", "created_at", "updated_at", "place_id"]
    for key, value in response.items():
        if key not in attributes:
            setattr(review, key, value)

    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
