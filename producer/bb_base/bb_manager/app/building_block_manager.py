from flask import Flask, flash, request, redirect, url_for, jsonify
import json
import sys
import requests
import time
import os
import socket
import threading
from zipfile import ZipFile
from django.utils.crypto import get_random_string #POSTERIORMENTE CAMBIAR A CADENA GENERADA POR NOSOTROS
import hashlib
from datetime import datetime

import db_manager

app = Flask(__name__)

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
API_NAME = os.environ['SERVICE_NAME']
DB_DATABASE = os.environ['DB_DATABASE']

sc_ip = ""
sc_port = ""

building_block_id_global = None

ip_blockchain = '148.247.201.227'

data_manager = db_manager.db_manager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)


def get_timestamp():
    datetimeObj = datetime.now()
    timeStampStr = datetimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
    return timeStampStr

#@app.before_first_request
def get_building_block_id():
	global building_block_id_global

	"""
	INSERT A BUILDING_BLOCK REGISTER
	"""
	#id_bb = get_random_string(length=80)
	#name_b = "my first building block"
	#address_b = "148.247.204.88"
	#port = 8002
	#dockerfile = "my first docker file"
	#volume_in_path = "my first volume in path"
	#volume_out_path = "my first volume out path"
	#result_insert_bb = data_manager.insert_building_block(id_bb, name_b, address_b, port, dockerfile, volume_in_path, volume_out_path)

	#print("EL ID DEL BB ES: " + str(result_insert_bb))

	#for i in range(0,4):
	#	id_stage = get_random_string(length=80)
	#	name_s = "stage number " + str(i)
	#	executable_sentence = "ex sentence number " + str(i)
	#	result_insert_stage = data_manager.insert_stage(id_stage, name_s, executable_sentence)

	building_block_id_global = data_manager.get_building_block_id()
	print("THE BUILDING BLOCK ID IS: " + str(building_block_id_global))
	result = createCatalogs('./DaemonOutputs')

@app.route('/saveFile/', methods=['POST'])
def  saveFile():
	'Receives the audio from our client and save it temporaly.'
	responder = {'status':'Not successfully'}
	if 'file' not in request.files:
		print("No existe archivo")
	file = request.files['file']

	if file.filename == '':
		print("El archivo no tiene nombre")

	if file:
		filename = file.filename
		file.save(os.path.join("./" + folder_in + "/", filename))
		print("File saved at " + folder_in)
		time.sleep(2)
		os.system("python node.py " + destination_data[0] + " " + destination_data[1] + " " + folder_in + " " + folder_out + " " + filename) #ip, port, in, out
		responder = {'status':'OK'}
	return json.dumps({'status':'OK', 'value chains':my_VC})

def createCatalogs(catalog):
	result = 0
	try:
		os.makedirs(catalog)
		result = 1
	except OSError as e:
		print("ERROR [Creating catalog]: " + catalog + "---" + str(e))
	return result

@app.route('/')
def home():
	h = {'api_name':API_NAME}
	return jsonify(h),200

@app.route('/transaction_auth', methods=['POST'])
def transaction_auth():
	pass

@app.route('/add_vc', methods=['POST'])
def add_vc():
	params = request.json
	print(params)
	contract_id = params['contract_id']
	transaction_id = params['transaction_id']
	value_chain_id = get_random_string(length=80)
	valid_contract = '1'
	result = data_manager.insert_value_chain(value_chain_id, contract_id, valid_contract, transaction_id)
	return jsonify(result),200

@app.route('/add_orders', methods=['POST'])
def add_orders():
	params = request.json
	id_order = params['id_order']
	status = params['status_o']
	transaction_id = params['transaction_id']
	content_id = params['content_id']
	logistic = params['logistic']
	file_name = params['file_name']
	iden = params['iden']
	result = data_manager.insert_order(id_order, status, transaction_id, content_id, logistic, file_name, iden)
	if(result):
		return jsonify(result),200
	else:
		return jsonify(result),500

@app.route('/f', methods=['POST'])
def f():
	"""
	Temporal method to test the transaction_authentication
	"""
	params = request.json
	transaction_id = params['transaction_id']
	result = data_manager.transaction_authentication(transaction_id)
	return jsonify(result),200

@app.route('/insert_stage', methods=['POST'])
def insert_stage():
	params = request.json
	id = params['identification']
	#id = get_random_string(length=80)
	name_s = params['name_s']
	executable_sentence = params['executable_sentence']
	result = data_manager.insert_stage(id, name_s, executable_sentence)
	return jsonify(result),200

@app.route('/insert_building_block', methods=['POST'])
def insert_building_block():
	params = request.json
	id = params['identification']
	#id = get_random_string(length=80)
	name_b = params['name_b']
	address_b = params['address_b']
	port = params['port']
	result = data_manager.insert_building_block(id, name_b, address_b, port)
	building_block_id_global = id
	result2 = createCatalogs('./DaemonOutputs')

	return jsonify(result),200


@app.route('/insert_vc_stage', methods=['POST'])
def insert_vc_stage():
	params = request.json
	value_chain_id = params['value_chain_id']
	stage_id = params['stage_id']
	folder_in = params['folder_in']
	folder_out = params['folder_out']
	result = data_manager.insert_vc_stage(value_chain_id, stage_id, folder_in, folder_out)
	return jsonify(result),200

@app.route('/get_stages')
def get_stages():
	result = data_manager.get_stages()
	#building_block_id_global = data_manager.get_building_block_id()
	return jsonify(result),200

def create_vc_stages(vc_id, volume_in_path, volume_out_path, transaction_id):
	stages = data_manager.get_stages()
	counter = 0

	if(len(stages) == 0):
		print("ERROR [create_vc_stage]: There are no stages registered in the building block")
		return 0
	elif(len(stages) == 1):
		counter += data_manager.insert_vc_stage(vc_id, stages[0][0], volume_in_path, volume_out_path)
		sentence = "nohup python -u content_daemon_building_block.py " + volume_in_path + " 4 " + stages[0][0] + " " + stages[0][1] + " push " + volume_out_path + " \
			" + stages[0][2] + "  " + DB_USER + " " + DB_PASSWORD + " " + DB_HOST + " "  + DB_PORT + " " + DB_DATABASE + " 0" + " " + sc_ip + " " + str(sc_port) + " " + transaction_id + " > ./DaemonOutputs/content_daemon_" + str(vc_id) + "_" + stages[0][1].split(".")[0]  + " &"
		os.system(sentence)
		return 1
	elif (len(stages)>1):

		folder_out = "./catalogs/building_block/" + vc_id + "/" + get_random_string(length=40)
		if(createCatalogs(folder_out)):
			counter += data_manager.insert_vc_stage(vc_id, stages[0][0], volume_in_path, folder_out)
			
			sentence = "nohup python -u content_daemon_building_block.py " + volume_in_path + " 4 " + stages[0][0] + " " + stages[0][1] + " push " + folder_out + " \
					" + stages[0][2] + "  " + DB_USER + " " + DB_PASSWORD + " " + DB_HOST + " "  + DB_PORT + " " + DB_DATABASE + " 0" + " " + sc_ip + " " + str(sc_port) + " " + transaction_id + " > ./DaemonOutputs/content_daemon_" + str(vc_id) + "_" + stages[0][1].split(".")[0]  + " &"
			os.system(sentence)

			print("CHECK 5: " + stages[0][0])

			for i in range(1, len(stages)-1):
				print("CHECK 6," + str(i) + ": " + stages[i][0])
				folder_in = folder_out
				folder_out = "./catalogs/building_block/" + vc_id + "/" + get_random_string(length=40)
				if(createCatalogs(folder_out)):
					counter += data_manager.insert_vc_stage(vc_id, stages[i][0], folder_in, folder_out)
					
					sentence = "nohup python -u content_daemon_building_block.py " + folder_in + " 4 " + stages[i][0] + " " + stages[i][1] + " push " + folder_out + " \
							" + stages[i][2] + "  " + DB_USER + " " + DB_PASSWORD + " " + DB_HOST + " "  + DB_PORT + " " + DB_DATABASE + " 0" + " " + sc_ip + " " + str(sc_port) + " " + transaction_id + " > ./DaemonOutputs/content_daemon_" + str(vc_id) + "_" + stages[i][1].split(".")[0]  + " &"
					os.system(sentence)

			
			folder_in = folder_out
			folder_out = volume_out_path
			print("CHECK 7: " + stages[len(stages)-1][0])
			counter += data_manager.insert_vc_stage(vc_id, stages[len(stages)-1][0], folder_in, folder_out)
			
			sentence = "nohup python -u content_daemon_building_block.py " + folder_in + " 4 " + stages[len(stages)-1][0] + " " + stages[len(stages)-1][1] + " push " + folder_out + " \
					" + stages[len(stages)-1][2] + "  " + DB_USER + " " + DB_PASSWORD + " " + DB_HOST + " "  + DB_PORT + " " + DB_DATABASE + " 0" + " " + sc_ip + " " + str(sc_port) + " " + transaction_id + " > ./DaemonOutputs/content_daemon_" + str(vc_id) + "_" + stages[len(stages)-1][1].split(".")[0]  + " &"
			os.system(sentence)


			if(counter==len(stages)):
				return volume_out_path
			else:
				return 0


@app.route('/deleteAll', methods=['POST'])
def deleteAll():
	counter = 0
	try:
		os.system("rm -r ./DaemonOutputs/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete DaemonOutputs")
	
	try:
		os.system("rm -r ./catalogs/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete catalogs")

	try:
		os.system("rm -r ./logs/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete logs")

	try:
		os.system("rm -r ./Outputs_Files/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete Outputs_Files")
	
	try:
		os.system("rm -r ./tiempos/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete tiempos")

	if(counter > 0):
		return "Something was deleted"
	else:
		return "Nothing was deleted"



@app.route('/add_value_chain', methods=['POST'])
def add_value_chain():
	global sc_ip
	global sc_port
	params = request.json
	vc_id = params['vc_id']
	contract_id = params['contract_id']
	valid_contract = params['valid_contract']
	transaction_id = params['transaction_id']
	sc_catalog_out = params['sc_catalog_out']
	sc_ip = params['sc_ip']
	sc_port = params['sc_port']
	volume_in_path = "./catalogs/building_block/" + vc_id + "/In_" + get_random_string(length=40)
	volume_out_path = "./catalogs/building_block/" + vc_id + "/Out_" +  get_random_string(length=40)
	global_result = False
	if(createCatalogs(volume_in_path) and createCatalogs(volume_out_path)): # Creation of the intra building block catalogs
		result = data_manager.add_value_chain(vc_id, contract_id, valid_contract, transaction_id,
			volume_in_path, volume_out_path)
		if(result):
			vc_stages_result = create_vc_stages(vc_id, volume_in_path, volume_out_path, transaction_id)
			if(result == 0):
				print("ERROR [Manager create_vc_stages]: Database record failed, try again the contract - " + str(contract_id))
				global_result = False
			else:
				sentence = "nohup python -u content_daemon_building_block.py " + volume_out_path + " 4 " + "s_id s_name " + "push " + sc_catalog_out + " \
							" + "e_sentence " + DB_USER + " " + DB_PASSWORD + " " + DB_HOST + " "  + DB_PORT + " " + DB_DATABASE + " 1" + " " + sc_ip + " " + str(sc_port) + " " + transaction_id +  " > ./DaemonOutputs/content_daemon_out" + str(vc_id)  + " &"
				print("CHECK FERNANDO: " + sentence)
				os.system(sentence)
				global_result = volume_in_path
		else:
			print("ERROR [Manager add_value_chain]: Database record failed, try again the contract - " + str(contract_id))
			global_result = False
	else:
		print("ERROR [Manager Creation of catalogs]: Intra building blocks catalogs creation error" + str(contract_id))
		global_result = False
	return global_result

if __name__ == '__main__':
	#building_block_id_global = data_manager.get_building_block_id()
	app.run(host='0.0.0.0', port=5000,debug = True)