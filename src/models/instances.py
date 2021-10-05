from src.app import docker_client, logger, config

class Factory:

	volume_name = "ovpn_volume"
	build_name = "wet_ladder"

	def setup(ca_key_passphrase, port, proto):

		common_name = "WetLadderVPN"

		docker_client.volumes.prune()

		volume_name = Factory.volume_name

		ovpn_volume = docker_client.volumes.create(name=volume_name)

		#build custom image with scripts to pipe to stdin
		logger.info("Building wet_ladder image!")
		build_name = Factory.build_name
		docker_client.images.build(path=".", tag=build_name)

		#generate config
		logger.info("Generating ovpn config!")
		genconfig_cmd = f"ovpn_genconfig -u {proto}://{config['VPN_HOST']}:{port}"
		res = docker_client.containers.run(build_name, genconfig_cmd, remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#create ca related files
		logger.info("Running initpki!")
		res = docker_client.containers.run(build_name, f"/bin/bash /initpki.sh {ca_key_passphrase} {common_name}", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
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