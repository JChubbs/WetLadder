from src.app import docker_client, logger, config, db

class Factory:

	def create_instance(build_name, ca_key_passphrase, port, proto):

		volume_name = f"{build_name}_volume"

		docker_client.volumes.prune()

		ovpn_volume = docker_client.volumes.create(name=volume_name)

		#build custom image with scripts to pipe to stdin
		logger.info("Building wet_ladder image!")
		docker_client.images.build(path=".", tag=build_name)

		#generate config
		logger.info("Generating ovpn config!")
		genconfig_cmd = f"ovpn_genconfig -u {proto}://{config['VPN_HOST']}:{port}"
		res = docker_client.containers.run(build_name, genconfig_cmd, remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#create ca related files
		logger.info("Running initpki!")
		res = docker_client.containers.run(build_name, f"/bin/bash /initpki.sh {ca_key_passphrase} {build_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#start vpn service
		logger.info("Starting VPN Service!")
		vpn_service = docker_client.containers.run(
			build_name, 
			detach=True, 
			ports={f"{port}/{proto}": int(port)}, 
			cap_add=["NET_ADMIN"], 
			volumes=[f"{volume_name}:/etc/openvpn"]
		)

		# add info to db
		cur = db.cursor()
		cur.execute("""
			INSERT INTO instances
			VALUES
			(?, ?, ?, ?, ?)
		""", (build_name, vpn_service.id, port, proto, volume_name))
		cur.close()

		db.commit()
		return build_name

	def delete_instance(build_name):
		container = Factory.get_container(build_name)
		container.stop()
		container.remove()

		cur = db.cursor()
		cur.execute("""
			DELETE FROM instances
			WHERE id = ?
		""", (build_name,))
		cur.close()
		db.commit()

	def get_volume(build_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT
				volume_name
			FROM instances
			WHERE id = ?
		""", (build_name,))
		volume_name = res.fetchone()[0]
		cur.close()
		return volume_name

	def get_container(build_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT
				container_id
			FROM instances
			WHERE id = ?
		""", (build_name,))

		container_id = res.fetchone()[0]
		container = docker_client.containers.get(container_id)
		cur.close()
		return container

	def get_all_instances():
		cur = db.cursor()
		res = cur.execute("""
			SELECT *
			FROM instances;
		""")
		out = [{"id": i[0], "container_id": i[1], "port": i[2], "protocol": i[3], "volume_name": i[4]} for i in res.fetchall()]
		cur.close()
		return out

	def get_instance(build_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT *
			FROM instances
			WHERE id = ?;
		""", (build_name,))
		out = res.fetchone()
		cur.close()
		return {"id": out[0], "container_id": out[1], "port": out[2], "protocol": out[3], "volume_name": out[4]}