from src.app import docker_client, config, db
from src.models.instances import Factory
from src.clientManager.clientManager import Target, ClientManager
import logging
import os

class Clients:

	def create(build_name, ca_key_passphrase, client_name, obfuscator_id=None):
		if not build_name or not ca_key_passphrase or not client_name:
			err = f"Invalid client creation paramaters build_name={build_name} client_name={client_name}"
			logging.exception(err)
			raise Exception(err) 

		cur = db.cursor()

		if obfuscator_id:
			#verify obfuscator belongs to instance
			cur.execute("SELECT instance_id FROM obfuscators WHERE id = ? AND instance_id = ?", (obfuscator_id, build_name))
			if cur.fetchone() is None:
				err = f"Invalid obfuscator_id={obfuscator_id} for build_name={build_name}"
				logging.exception(err)
				Exception(err)

		volume_name = Factory.get_volume(build_name)

		docker_client.containers.run(build_name, f"/bin/bash /build_client.sh {ca_key_passphrase} {client_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])

		cur.execute("""
			INSERT INTO clients
			VALUES
			(?, ?, ?)
		""", (client_name, build_name, obfuscator_id))

		cur.close()

		db.commit()

	def get_config(build_name, client_name):
		volume_name = Factory.get_volume(build_name)

		contents = docker_client.containers.run(build_name, f"ovpn_getclient {client_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		with open(f"./tmp/{client_name}.ovpn", "wb") as f_writer:
			f_writer.write(contents)

		return f"./tmp/{client_name}.ovpn"

	def get_client(
		build_name: str,
		client_name: str, 
		target: Target
		):

		if not ClientManager.client_config_exists(client_name):
			logging.info(f"client config file doesn't exist for {client_name} - retrieving")
			Clients.get_config(build_name, client_name)

		return ClientManager.build_client(target, client_name)

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
				id,
				instance_id,
				obfuscator_id
			FROM clients
			WHERE instance_id = ?
		""", (build_name,))
		out = [{"id": i[0], "instance_id": i[1], "obfuscator_id": i[2]} for i in res.fetchall()]
		cur.close()
		return out

	def get(build_name, client_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT 
				id,
				instance_id,
				obfuscator_id
			FROM clients
			WHERE instance_id = ?
			AND id = ?
		""", (build_name, client_name))

		out = res.fetchone()
		cur.close()
		return {"id": out[0], "instance_id": out[1], "obfuscator_id": out[2]}