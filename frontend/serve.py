#!/usr/bin/env python3
"""
Backend service for the singular frontend
Presently will probably just handle the settings.json file
"""
import os
import json
import time
import shutil

from flask import Flask, render_template
from flask  import request
from flask_cors import CORS



SETTINGS_FILE = "../../settings.json" # TODO: Change this properly
if "SINGULAR_SETTINGS_FILE" in os.environ:
    SETTINGS_FILE = os.environ["SETTINGS_FILE"]

app = Flask(__name__
        )
CORS(app)

@app.route("/get")
def return_settings():
    """Returns the output of settings.json"""
    with open(SETTINGS_FILE) as f:
        return json.dumps(json.load(f))

@app.route("/save", methods=["POST"])
def save_settings():
    """Saves the settings.json file"""
    data = request.get_json(force=True)

    # Copy the SETTINGS file to backup
    shutil.copyfile(SETTINGS_FILE, SETTINGS_FILE + "." + str(time.time()))

    with open(SETTINGS_FILE, "r+") as f:
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return "Saved."

if __name__ == "__main__":
    app.debug = True
    app.config["ENV"] = "development"
    app.run(host="0.0.0.0")
