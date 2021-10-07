from src.app import docker_client, config, db
from src.models.instances import Factory
import os
import json

class Clients:

	def create(build_name, ca_key_passphrase, client_name):
		volume_name = Factory.get_volume(build_name)

		docker_client.containers.run(build_name, f"/bin/bash /build_client.sh {ca_key_passphrase} {client_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])

		cur = db.cursor()
		cur.execute("""
			INSERT INTO clients
			VALUES
			(?, ?)
		""", (client_name, build_name))

		cur.close()

		db.commit()

	def get_config(build_name, client_name):
		volume_name = Factory.get_volume(build_name)

		contents = docker_client.containers.run(build_name, f"ovpn_getclient {client_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		with open(f"./tmp/{client_name}.ovpn", "wb") as f_writer:
			f_writer.write(contents)

		return f"./tmp/{client_name}.ovpn"

	def delete(build_name, client_name):
		volume_name = Factory.get_volume(build_name)

		docker_client.containers.run(build_name, f"/bin/bash /delete_client.sh {client_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])

		cur = db.cursor()
		cur.execute("""
			DELETE FROM clients
			WHERE instance_id = ?
			AND id = ?
		""", (build_name, client_name))

		cur.close()
		db.commit()

	def get_all(build_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT
				json_object('id', id, 'instance_id', instance_id)
			FROM clients
			WHERE instance_id = ?
		""", (build_name,))

		out = [json.loads(i[0]) for i in res.fetchall()]
		cur.close()
		return out

	def get(build_name, client_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT
				json_object('id', id, 'instance_id', instance_id)
			FROM clients
			WHERE instance_id = ?
			AND id = ?
		""", (build_name, client_name))

		out = res.fetchone()
		cur.close()
		return out[0]