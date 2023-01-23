#!/usr/bin/python3
"""
creating route
"""
from api.v1.views import app_views
import json
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """status"""
    return jsonify(status="OK")


@app_views.route('/stats')
def counting():
    """retrieve and count"""
    return jsonify(amenities=storage.count('Amenity'),
                   cities=storage.count('City'),
                   places=storage.count('Place'),
                   reviews=storage.count('Review'),
                   states=storage.count('State'),
                   users=storage.count('User'))
