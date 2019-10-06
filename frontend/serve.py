#!/usr/bin/env python3
"""
Backend service for the singular frontend
Presently will probably just handle the settings.json file
"""
import os
import json

from flask import Flask
from flask  import request
from flask_cors import CORS



SETTINGS_FILE = "../../settings.json" # TODO: Change this properly
if "SINGULAR_SETTINGS_FILE" in os.environ:
    SETTINGS_FILE = os.environ["SETTINGS_FILE"]

app = Flask("singular_frontend")
CORS(app)

@app.route("/get")
def return_settings():
    """Returns the output of settings.json"""
    with open(SETTINGS_FILE) as f:
        return json.dumps(json.load(f))

if __name__ == "__main__":
    app.debug = True
    app.config["ENV"] = "development"
    app.run()
