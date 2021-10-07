from src.app import app
from src.models.clients import Clients
from flask import request, send_file

@app.route("/instances/<instance_id>/clients", methods=["GET"])
def get_all_clients(instance_id):
	res = Clients.get_all(instance_id)
	return {"clients": res}

@app.route("/instances/<instance_id>/clients/<client_id>", methods=["GET"])
def get_a_client(instance_id, client_id):
	action = request.args.get("action")
	if action == "download":
		file = Clients.get_config(instance_id, client_id)
		return send_file(file, attachment_filename=f"{client_id}.ovpn")
	else:
		res = Clients.get(instance_id, client_id)
		return res

@app.route("/instances/<instance_id>/clients", methods=["POST"])
def create_a_client(instance_id):
	ca_key_passphrase = request.json["ca_key_passphrase"]
	client_name = request.json["client_name"]
	Clients.create(instance_id, ca_key_passphrase, client_name)
	file = Clients.get_config(instance_id, client_name)
	return send_file(file, attachment_filename=f"{client_name}.ovpn")

@app.route("/instances/<instance_id>/clients/<client_id>", methods=["DELETE"])
def delete_a_client(instance_id, client_id):
	Clients.delete(instance_id, client_id)
	return {"status": "success"}