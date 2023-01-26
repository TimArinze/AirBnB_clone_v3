#!/usr/bin/python3
"""
Instance of flask
"""
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error handling"""
    return make_response(jsonify(error='Not found'), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
