from src.app import app
from flask import request
from src.models.instances import Factory

@app.route("/instances", methods=["GET"])
def get_all_instances():
	instances = Factory.get_all_instances()
	return {"instances": instances}

@app.route("/instances/<instance_id>", methods=["GET"])
def get_instance(instance_id):
	instance = Factory.get_instance(instance_id)
	return instance

@app.route("/instances", methods=["POST"])
def create_an_instance():
	try:
		name = request.json["name"]
		ca_key_passphrase = request.json["ca_key_passphrase"]
		port = request.json["port"]
		proto = request.json["proto"]
	except:
		{"status": "failed"}

	instance_id = Factory.create_instance(name, ca_key_passphrase, port, proto)
	return {"instance_id": instance_id}

@app.route("/instances/<instance_id>", methods=["DELETE"])
def delete_an_instance(instance_id):
	Factory.delete_instance(instance_id)
	return {"sucess": f"{instance_id} instance deleted"}