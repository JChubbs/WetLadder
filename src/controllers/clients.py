from src.app import app
from src.models.clients import Clients
from flask import request, send_file

@app.route("/clients", methods=["POST"])
def create_a_client():
	client_name = request.json["client_name"]
	Clients.create(client_name)
	file = Clients.get(client_name)
	return send_file(file, attachment_filename=f"{client_name}.ovpn")

@app.route("/clients", methods=["DELETE"])
def delete_a_client():
	client_name = request.json["client_name"]
	Clients.delete(client_name)
	return {"status": "success"}