#!/usr/bin/env python3
"""
Backend service for the singular frontend
Presently will probably just handle the settings.json file
"""
import os
import json
import time
import shutil
import docker

from flask import Flask, render_template, send_from_directory
from flask  import request
from flask_cors import CORS

SETTINGS_FOLDER = "../../"
if "SINGULAR_SETTINGS_FOLDER" in os.environ:
    SETTINGS_FOLDER = os.environ["SINGULAR_SETTINGS_FOLDER"]

SETTINGS_FILE = "settings.json" # TODO: Change this properly
if "SINGULAR_SETTINGS_FILE" in os.environ:
    SETTINGS_FILE = os.environ["SINGULAR_SETTINGS_FILE"]

DOCKER_NAME = "singular_cli"
if "SINGULAR_DOCKER_NAME" in os.environ:
    DOCKER_NAME = os.environ["SINGULAR_DOCKER_NAME"]

app = Flask(__name__,
        static_url_path="/"
        )
CORS(app)

# Static routes
@app.route("/js/<path:path>")
def send_js(path):  # pragma: no cover
    return send_from_directory("./dist/js", path)


@app.route("/css/<path:path>")
def send_css(path):  # pragma: no cover
    return send_from_directory("./dist/css", path)


@app.route("/img/<path:path>")
def send_img(path):  # pragma: no cover
    return send_from_directory("./dist/img", path)

@app.route("/")
def send_home(): #pragma: no cover
    return send_from_directory("./dist/", "index.html")

@app.route("/dist/<path:path>")
def send_dist(path):  # pragma: no cover
    return send_from_directory("./dist", path)



@app.route("/get")
def return_settings():
    """Returns the output of settings.json"""
    with open(SETTINGS_FOLDER + SETTINGS_FILE) as f:
        return json.dumps(json.load(f))

@app.route("/save", methods=["POST"])
def save_settings():
    """Saves the settings.json file"""
    data = request.get_json(force=True)

    # Copy the SETTINGS file to backup
    if not os.path.isdir(SETTINGS_FOLDER + "backup"):
        os.mkdir(SETTINGS_FOLDER + "backup")
    shutil.copyfile(SETTINGS_FOLDER + SETTINGS_FILE, SETTINGS_FOLDER + "backup/" + SETTINGS_FILE + "." + str(time.time()))

    with open(SETTINGS_FOLDER + SETTINGS_FILE, "r+") as f:
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return "Saved."

@app.route("/docker/status")
def docker_status():
    """Checks the docker status"""
    docker_env = docker.from_env()
    dockers = [ str(x.name) for x in docker_env.containers.list() ]
    if [ x for x in dockers if DOCKER_NAME in x ] == []:
        return str(dockers) + "<br /><br />Docker " + str(DOCKER_NAME) + " not running.", 410 # HTTP code gone
    
    matched_docker = [x for x in docker_env.containers.list() if DOCKER_NAME in str(x.name)][0]
    return matched_docker.logs().decode("utf-8")

@app.route("/docker/restart")
def docker_restart():
    """Restarts the given docker"""
    docker_env = docker.from_env()
    dockers = [str(x.name) for x in docker_env.containers.list(all=True)]
    if [ x for x in dockers if DOCKER_NAME in x ] == []:
        return str(dockers) + ", Docker " + str(DOCKER_NAME) + " not found", 410 # HTTP code gone

    matched_docker = [x for x in docker_env.containers.list() if DOCKER_NAME in str(x.name)][0]
    matched_docker.restart()
    return "Restarted"


if __name__ == "__main__":
    app.debug = True
    app.config["ENV"] = "development"
    app.run(host="0.0.0.0", port=7500)
