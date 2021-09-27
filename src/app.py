import flask
import docker
import decouple

app = flask.Flask("WetLadder-API")
app.config["DEBUG"] = True

#establish docker connection
docker_client = docker.from_env()

import src.controllers