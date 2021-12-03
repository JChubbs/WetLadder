import uuid
import json
import logging
import subprocess

from src.app import db

class Obfuscators:

	def get_all(instance_id):
		cur = db.cursor()
		res = cur.execute("""
			SELECT *
			FROM obfuscators
			WHERE instance_id = ?
		""", (instance_id,))
		out = [{"id": i[0], "instance_id": i[2], "obfuscation_method": i[1], "config": i[3], "listener_port": i[4]} for i in res.fetchall()]
		cur.close()
		return out

	def get(build_name, client_name):
		cur = db.cursor()
		res = cur.execute("""
			SELECT *
			FROM obfuscators
			WHERE instance_id = ?
			AND id = ?
		""", (build_name, client_name))

		out = res.fetchone()
		cur.close()
		return {"id": out[0], "instance_id": out[2], "obfuscation_method": out[1], "config": out[3], "listener_port": out[4]}

	def create(instance_id, listener_port: int, obfuscation_method):

		cur = db.cursor()

		#get listener port from instance
		cur.execute("""
			SELECT
				port,
				protocol
			FROM instances
			WHERE id = ?
		""", (instance_id,))

		res = cur.fetchone()

		fwd_port = res[0]
		fwd_proto = res[1]

		method_config = {}

		obfuscator_command = [
			"./shapeshifter-dispatcher/shapeshifter-dispatcher", 
			"-transparent",
			"-server", 
			"-orport", f"127.0.0.1:{fwd_port}", 
			"-transports", obfuscation_method,
			"-bindaddr", f"{obfuscation_method}-0.0.0.0:{listener_port}",
			"-ptversion", "2"
		]
		
		if obfuscation_method == "obfs2":
			pass

		else:
			msg = f"Obfuscation method {obfuscation_method} is not currently supported!"
			logging.exception(msg)
			raise Exception(msg) 

		#TODO test udp obfuscation
		if fwd_proto == "udp":
			obfuscator_command.append("-udp")

		# run shapeshifter-dispatcher
		process = subprocess.Popen(obfuscator_command)
		logging.info(process.pid)

		obfuscator_id = uuid.uuid1()

		cur.execute("""
			INSERT INTO obfuscators
			(id, obfuscation_method, instance_id, config, listener_port)
			VALUES
			(?, ?, ?, ?, ?)
		""", (str(obfuscator_id), obfuscation_method, instance_id, json.dumps(method_config), listener_port))

		cur.close()
		db.commit()

		return obfuscator_id