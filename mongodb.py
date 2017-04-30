#!/usr/bin/env python3
import io
import yaml # Note: pip3 install pyyaml
import pymongo
import json

CONFIG_FILE = 'mongodb.yml'

config = None
with io.open(CONFIG_FILE, 'r', encoding='utf8') as stream:
	config = yaml.load(stream)

def get_collection(name):
	try:
		client = pymongo.MongoClient(config['host'], config['port'])
		db = client[config['database']]
		return db[name]
	except Exception as e:
		print(str(e))

def insert(collection_name, document):
	try:
		collection = get_collection(collection_name)
		collection.insert_one(json.loads(document))

	except Exception as e:
		print(str(e))

def replace(collection_name, document):
	try:
		collection = get_collection(collection_name)
		collection.drop()	
		insert(collection_name, document)

	except Exception as e:
		print(str(e))
		


