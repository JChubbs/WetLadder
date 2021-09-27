import flask
import docker
import logging
from dotenv import dotenv_values

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = dotenv_values(".env")

app = flask.Flask("WetLadder-API")
app.config["DEBUG"] = True

#establish docker connection
docker_client = docker.from_env()

import src.controllers