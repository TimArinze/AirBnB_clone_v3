#!/usr/bin/python3
"""
Restful USer
"""
from flask import Flask, jsonify, abort, request
from models.user import User
import json
from api.v1.views import app_views
from models import storage
import hashlib


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieve all users"""
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def a_user(user_id):
    """Retrieve one user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """remove a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """new user"""
    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    if "email" not in response:
        abort(400, "Missing email")
    if "password" not in response:
        abort(400, "Missing password")
    user = User(**response)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a users info"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    response = request.get_json()
    if not response:
        abort(400, "Not a JSON")
    for key, value in response.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict(), 200)
