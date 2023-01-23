#!/usr/bin/python3
"""
creating route
"""
from api.v1.views import app_views
import json
from flask import jsonify


@app_views.route('/status')
def status():
    """status"""
    return jsonify(status="OK")
