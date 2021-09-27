from src.app import docker_client, logger, config
import os

class Factory:

	#TODO replace hardcoded vals
	temp_script_vars = {
		"ca_key_passphrase": "secure_passphrase",
		"common_name": "WetLadderVPN"
	}

	volume_name = "ovpn_volume"
	build_name = "wet_ladder"

	def replace_script_vars(script_lines):
		for key, val in Factory.temp_script_vars.items():
			script_lines = script_lines.replace(f"::{key}", val)
		return script_lines

	def build_scripts():
		scripts_out = {}
		for f in os.listdir("./script_templates"):
			with open(f"./script_templates/{f}", "r") as f_reader:
				lines = f_reader.read()
				scripts_out[f] = Factory.replace_script_vars(lines)

		for f, c in scripts_out.items():
			with open(f"./scripts/{f}", "w") as f_writer:
				f_writer.write(c)

	def setup():
		Factory.build_scripts()

		docker_client.volumes.prune()

		volume_name = Factory.volume_name

		ovpn_volume = docker_client.volumes.create(name=volume_name)

		#build custom image with scripts to pipe to stdin
		logger.info("Building wet_ladder image!")
		build_name = Factory.build_name
		docker_client.images.build(path=".", tag=build_name)

		#generate config
		logger.info("Generating ovpn config!")
		genconfig_cmd = f"ovpn_genconfig -u {config['VPN_PROTO']}://{config['VPN_HOST']}:{config['VPN_PORT']}"
		res = docker_client.containers.run(build_name, genconfig_cmd, volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#create ca related files
		logger.info("Running initpki!")
		res = docker_client.containers.run(build_name, "/bin/bash /initpki.sh", volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#start vpn service
		logger.info("Starting VPN Service!")
		vpn_service = docker_client.containers.run(
			build_name, 
			detach=True, 
			ports={f"{config['VPN_PORT']}/{config['VPN_PROTO']}": int(config["VPN_PORT"])}, 
			cap_add=["NET_ADMIN"], 
			volumes=[f"{volume_name}:/etc/openvpn"]
		)