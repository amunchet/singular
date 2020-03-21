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
import re
import sys

from flask import Flask, render_template, send_from_directory, stream_with_context, Response
from flask import request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_socketio import send, emit

import feedparser

SETTINGS_FOLDER = "../../"
if "SINGULAR_SETTINGS_FOLDER" in os.environ:
    SETTINGS_FOLDER = os.environ["SINGULAR_SETTINGS_FOLDER"]

SETTINGS_FILE = "settings.json"  # TODO: Change this properly
if "SINGULAR_SETTINGS_FILE" in os.environ:
    SETTINGS_FILE = os.environ["SINGULAR_SETTINGS_FILE"]

DOCKER_NAME = "singular_cli"
if "SINGULAR_DOCKER_NAME" in os.environ:
    DOCKER_NAME = os.environ["SINGULAR_DOCKER_NAME"]

app = Flask(__name__,
            static_url_path="/"
            )

FRONTEND_PATH = "/data/frontend/"

app.config["SECRET_KEY"] = "asdfzxcva43afaazvxc"
socketio = SocketIO(app)
CORS(app)

# Static routes
@app.route("/js/<path:path>")
def send_js(path):  # pragma: no cover
    return send_from_directory(FRONTEND_PATH + "dist/js", path)


@app.route("/css/<path:path>")
def send_css(path):  # pragma: no cover
    return send_from_directory(FRONTEND_PATH + "dist/css", path)


@app.route("/img/<path:path>")
def send_img(path):  # pragma: no cover
    return send_from_directory(FRONTEND_PATH + "dist/img", path)


@app.route("/")
def send_home():  # pragma: no cover
    return send_from_directory(FRONTEND_PATH + "dist/", "index.html")


@app.route("/dist/<path:path>")
def send_dist(path):  # pragma: no cover
    return send_from_directory(FRONTEND_PATH + "dist", path)


@app.route("/get")
def return_settings():
    """Returns the output of settings.json"""
    if not os.path.exists(SETTINGS_FOLDER + SETTINGS_FILE):
        with open(SETTINGS_FOLDER + SETTINGS_FILE, "w") as f:
            output = "{\"shows\":[],\"rss_feed\": []}"
            f.write(output)
            return output

    with open(SETTINGS_FOLDER + SETTINGS_FILE) as f:
        return json.dumps(json.load(f))


@app.route("/rss")
def return_rss():
    """Retrieves and returns the RSS feeds top 5"""
    if not os.path.exists(SETTINGS_FOLDER + SETTINGS_FILE):
        return "Cannot find settings.json", 409

    settings = ''
    with open(SETTINGS_FOLDER + SETTINGS_FILE) as f:
        settings = json.load(f)

    retval = {}
    for feed in settings['rss_feed']:
        a = feedparser.parse(feed)
        retval[feed] = [re.sub(r'[\(\[].*?[\)\]]', '', x['title']
                               ).split('-')[0].strip()[:10] for x in a.entries[:5]]

    return json.dumps(retval), 200


@app.route("/save", methods=["POST"])
def save_settings():
    """Saves the settings.json file"""
    data = request.get_json(force=True)

    # Copy the SETTINGS file to backup
    if not os.path.isdir(SETTINGS_FOLDER + "backup"):
        os.mkdir(SETTINGS_FOLDER + "backup")
    shutil.copyfile(SETTINGS_FOLDER + SETTINGS_FILE, SETTINGS_FOLDER +
                    "backup/" + SETTINGS_FILE + "." + str(time.time()))

    with open(SETTINGS_FOLDER + SETTINGS_FILE, "r+") as f:
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    return "Saved."

# Docker section


@app.route("/docker/status")
def docker_status():
    """Checks the docker status"""
    docker_env = docker.from_env()
    dockers = [str(x.name) for x in docker_env.containers.list()]
    if [x for x in dockers if DOCKER_NAME in x] == []:
        # HTTP code gone
        return str(dockers) + "<br /><br />Docker " + str(DOCKER_NAME) + " not running.", 410

    matched_docker = [x for x in docker_env.containers.list()
                      if DOCKER_NAME in str(x.name)][0]

    def generate():
        yield matched_docker.logs(stream=True).next().decode("utf-8")
    return Response(stream_with_context(generate()))
    # return matched_docker.logs(stream=True).next().decode("utf-8")


@socketio.on('message')
def handle_message(message):
    emit("response", "Received " + str(message))

# @app.route("/docker/restart")
@socketio.on('restart')
def docker_restart():
    """Restarts the given docker"""
    docker_env = docker.from_env()
    dockers = [str(x.name) for x in docker_env.containers.list(all=True)]
    if [x for x in dockers if DOCKER_NAME in x] == []:
        emit("response", "ERROR: " + str(dockers) +
             ", Docker " + str(DOCKER_NAME) + " not found")

    matched_docker = [x for x in docker_env.containers.list(
        all=True) if DOCKER_NAME in str(x.name)][0]
    matched_docker.restart()
    emit("response", "Docker Restarted.")

    matched_docker = [x for x in docker_env.containers.list()
                      if DOCKER_NAME in str(x.name)][0]

    for line in matched_docker.logs(stream=True):
        emit("response", str(line.strip()))

    emit("response", "Docker finished.")


if __name__ == "__main__":
    #app.debug = True
    #app.config["ENV"] = "development"
    #app.run(host="0.0.0.0", port=7500)

    if len(sys.argv) < 2:
        socketio.run(app, host="0.0.0.0", port=7500)
    else:
        socketio.run(app, host="0.0.0.0", port=int(sys.argv[1]))
