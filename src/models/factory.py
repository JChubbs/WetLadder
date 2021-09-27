from src.app import docker_client
from src.config.config import *
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
		for f in os.listdir(SCRIPT_TEMPLATES):
			with open(f"SCRIPT_TEMPLATES/{f}", "r") as f_reader:
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
		build_name = Factory.build_name
		docker_client.images.build(path=".", tag=build_name)

		#generate config
		genconfig_cmd = f"ovpn_genconfig -u {VPN_PROTO}://{VPN_HOST}:{VPN_PORT}"
		docker_client.containers.run(build_name, genconfig_cmd, volumes=[f"{volume_name}:/etc/openvpn"])

		#create ca related files
		docker_client.containers.run(build_name, "/bin/bash /initpki.sh", volumes=[f"{volume_name}:/etc/openvpn"])

		#start vpn service
		vpn_service = docker_client.containers.run(
			build_name, 
			detach=True, 
			ports={f"{VPN_PORT}/{VPN_PROTO}": int(VPN_PORT)}, 
			cap_add=["NET_ADMIN"], 
			volumes=[f"{volume_name}:/etc/openvpn"]
		)