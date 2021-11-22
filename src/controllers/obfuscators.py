from src.app import app
from src.models.obfuscators import Obfuscators
from flask import request

@app.route("/instances/<instance_id>/obfuscators", methods=["GET"])
def get_all_obfuscators(instance_id):
	res = Obfuscators.get_all(instance_id)
	return {"obfuscators": res}

@app.route("/instances/<instance_id>/obfuscators/<obfuscator_id>", methods=["GET"])
def get_a_obfuscators(instance_id, obfuscator_id):
	res = Obfuscators.get(instance_id, obfuscator_id)
	return res

@app.route("/instances/<instance_id>/obfuscators", methods=["POST"])
def create_a_obfuscators(instance_id):
	listener_port = request.json["listener_port"]
	obfuscation_method = request.json["obfuscation_method"]
	obfuscator_id = Obfuscators.create(instance_id, listener_port, obfuscation_method)
	return {"obfuscator_id": obfuscator_id}

"""
@app.route("/instances/<instance_id>/obfuscators/<obfuscator_id>", methods=["DELETE"])
def delete_a_obfuscators(instance_id, obfuscator_id):
	Obfuscators.delete(instance_id, obfuscator_id)
	return {"status": "success"}

"""