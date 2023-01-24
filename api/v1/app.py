#!/usr/bin/python3
"""
Instance of flask
"""
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST') or '0.0.0.0'
    port = os.environ.get('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
