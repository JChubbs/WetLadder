from src.app import app
from flask import request
from src.models.instances import Factory

@app.route("/instances", methods=["POST"])
def create_an_instance():
	try:
		ca_key_passphrase = request.json["ca_key_passphrase"]
		port = request.json["port"]
		proto = request.json["proto"]
	except:
		{"status": "failed"}

	Factory.setup(ca_key_passphrase, port, proto)
	return {"status": "success"}