import os
import shutil
import logging
import subprocess
from enum import Enum

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

		#create folder in tmp folder
		client_dir = f"./tmp/{client_name}"
		if os.path.exists(client_dir): shutil.rmtree(client_dir)
		os.mkdir(client_dir)
		os.mkdir(f"{client_dir}/config")

		if target == Target.WIN_64:
			#build client for target
			os.environ["GOOS"] = "windows"
			os.environ["GOARCH"] = "386"
			p = subprocess.Popen(["go", "build", "-o", f"../{client_dir}", "internal/client/WetLadder-Client.go"], cwd="WetLadder-Client")
			#os.system(f"GOOS=windows GOARCH=386 go build -o {client_dir} WetLadder-Client/internal/client/WetLadder-Client.go")
			shutil.copytree("WetLadder-Client/win-64", f"{client_dir}/win-64")
			shutil.copyfile(f"./tmp/{client_name}.ovpn", f"{client_dir}/config/{client_name}.ovpn")
			with open(f"{client_dir}/.env", "w") as dotenv_f:
				dotenv_f.write("EXECUTABLE_PATH=win-64/openvpn.exe\n")
				dotenv_f.write(f"OPENVPN_CONFIG=config/{client_name}.ovpn\n")
				dotenv_f.write("PLATFORM=win-64\n")	
			#wait for go build to finish
			p.wait()
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