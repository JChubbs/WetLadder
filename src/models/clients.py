from src.app import docker_client, config
from src.models.factory import Factory
import os

class Clients:

	def create(client_name):
		volume_name = Factory.volume_name
		build_name = Factory.build_name

		docker_client.containers.run(build_name, f"/bin/bash /build_client.sh {client_name}", volumes=[f"{volume_name}:/etc/openvpn"])

	def get(client_name):
		volume_name = Factory.volume_name
		build_name = Factory.build_name

		contents = docker_client.containers.run(build_name, f"ovpn_getclient {client_name}", volumes=[f"{volume_name}:/etc/openvpn"])
		with open(f"./tmp/{client_name}.ovpn", "wb") as f_writer:
			f_writer.write(contents)

		return f"./tmp/{client_name}.ovpn"

	def delete(client_name):
		volume_name = Factory.volume_name
		build_name = Factory.build_name

		docker_client.containers.run(build_name, f"/bin/bash /delete_client.sh {client_name}", volumes=[f"{volume_name}:/etc/openvpn"])