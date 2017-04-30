#!/usr/bin/env python3
import subprocess
import json

def sh(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	out, err = process.communicate()
	if err is not None:
		raise Exception('Error while process ' + command)
	else:
		return out.decode('utf-8').strip()

def jsony(obj):
	class Encoder(json.JSONEncoder):
		def default(self, obj):
			return obj.__dict__

	return str(json.dumps(obj, cls=Encoder))



