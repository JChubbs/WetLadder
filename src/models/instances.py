from src.app import docker_client, logger, config
import os

class Factory:

	volume_name = "ovpn_volume"
	build_name = "wet_ladder"

	def replace_script_vars(script_lines, vars):
		for key, val in vars.items():
			script_lines = script_lines.replace(f"::{key}", val)
		return script_lines

	def build_scripts(vars):
		scripts_out = {}
		for f in os.listdir("./script_templates"):
			with open(f"./script_templates/{f}", "r") as f_reader:
				lines = f_reader.read()
				scripts_out[f] = Factory.replace_script_vars(lines, vars)

		for f, c in scripts_out.items():
			with open(f"./scripts/{f}", "w") as f_writer:
				f_writer.write(c)

	def setup(ca_key_passphrase, port, proto):

		script_vars = {
			"ca_key_passphrase": ca_key_passphrase,
			"common_name": "WetLadderVPN"
		}

		Factory.build_scripts(script_vars)

		docker_client.volumes.prune()

		volume_name = Factory.volume_name

		ovpn_volume = docker_client.volumes.create(name=volume_name)

		#build custom image with scripts to pipe to stdin
		logger.info("Building wet_ladder image!")
		build_name = Factory.build_name
		docker_client.images.build(path=".", tag=build_name)

		#remove scripts
		for f in os.listdir("./scripts"):
			os.remove(os.path.join("./scripts", f))

		#generate config
		logger.info("Generating ovpn config!")
		genconfig_cmd = f"ovpn_genconfig -u {proto}://{config['VPN_HOST']}:{port}"
		res = docker_client.containers.run(build_name, genconfig_cmd, remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
		logger.info(res)

		#create ca related files
		logger.info("Running initpki!")
		res = docker_client.containers.run(build_name, "/bin/bash /initpki.sh", remove=True, volumes=[f"{volume_name}:/etc/openvpn"])
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