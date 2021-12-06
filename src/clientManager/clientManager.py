import os
import shutil
import logging
from enum import Enum

from src.app import config
from src.models.obfuscators import Obfuscators

class Target(Enum):
	#WIN_32 = "win-32"
	WIN_64 = "win-64"
	NIX    = "nix"
	#ARM    = "arm-linux-gnueabi"


class ClientManager:

	def client_config_exists(
		client_name: str
		) -> bool:

		return os.path.exists(f"./tmp/{client_name}.ovpn")

	def build_client(
		target: Target,
		client_name: str
		):

		#ensure client config exists
		if not ClientManager.client_config_exists(client_name):
			err = f"Client config does not exist for {client_name}"
			logging.exception(err)
			raise Exception(err)

		#check for obfuscation
		obfuscation_settings = Obfuscators.get_client_obfuscator(client_name)
		obfuscation_set = obfuscation_settings.get("obfuscation_type") is not None

		#create folder in tmp folder
		client_dir = f"./tmp/{client_name}"
		if os.path.exists(client_dir): shutil.rmtree(client_dir)
		os.mkdir(client_dir)
		os.mkdir(f"{client_dir}/config")

		shutil.copyfile(f"./tmp/{client_name}.ovpn", f"{client_dir}/config/{client_name}.ovpn")

		if obfuscation_set:
			obfs_conf = ""
			#edit config file to no longer have remote addres and add route
			with open(f"{client_dir}/config/{client_name}.ovpn", "r") as conf_file:
				new_lines = []
				for line in conf_file.readlines():
					if not "remote " in line:
						new_lines.append(line)
				new_lines.append(f"route {config['VPN_HOST']} 255.255.255.255 net_gateway")
			with open(f"{client_dir}/config/{client_name}.ovpn", "w") as conf_file:
				for line in new_lines:
					conf_file.write(line)

			#create method specific config files
			if obfuscation_settings["obfuscation_type"] == "obfs4":
				obfs_conf = "config/obfs-conf.json"
				with open(f"{client_dir}/config/obfs-conf.json", "w") as obfs_conf_f:
					obfs_conf_f.write(obfuscation_settings["config"])

		if target == Target.WIN_64:
			shutil.copyfile("WetLadder-Client/client-builds/win-64/WetLadder-Client.exe", f"{client_dir}/WetLadder-Client.exe")

			shutil.copytree("WetLadder-Client/openvpn-builds/win-64", f"{client_dir}/win-64")
			with open(f"{client_dir}/.env", "w") as dotenv_f:
				dotenv_f.write("EXECUTABLE_PATH=win-64/openvpn.exe\n")
				dotenv_f.write(f"OPENVPN_CONFIG=config/{client_name}.ovpn\n")
				dotenv_f.write("PLATFORM=win-64\n")

			if obfuscation_set:
				shutil.copytree("WetLadder-Client/shapeshifter-builds/win-64", f"{client_dir}/shapeshifter")
				with open(f"{client_dir}/.env", "a") as dotenv_f:
					dotenv_f.write(f"OBFUSCATION_TYPE={obfuscation_settings['obfuscation_type']}\n")
					dotenv_f.write(f"OBFUSCATION_TARGET={obfuscation_settings['obfuscation_target']}\n")
					dotenv_f.write("OBFUSCATOR_PATH=shapeshifter/shapeshifter-dispatcher.exe\n")
					dotenv_f.write(f"OBFUSCATOR_CONFIG_PATH={obfs_conf}\n")

			#zip
			shutil.make_archive(f"{client_dir}", "zip", client_dir)
			out_file = f"{client_dir}.zip"

		elif target == Target.NIX:
			#TODO Setup Unix Stuff
			pass

		else:
			err = f"Invalid target {target}"
			logging.exception(err)
			raise Exception(err)

		#delete folder
		shutil.rmtree(client_dir)

		return out_file	