import flask
import docker
import logging
import sqlite3
from dotenv import dotenv_values

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = dotenv_values(".env")

app = flask.Flask("WetLadder-API")
app.config["DEBUG"] = True

#establish docker connection
docker_client = docker.from_env()

#establish db
db = sqlite3.connect("./wet_ladder.db", check_same_thread=False)

import src.controllers