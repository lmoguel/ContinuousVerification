from flask import Flask, flash, request, redirect, url_for, jsonify
import json
import sys
import requests
import time
import os
import errno
import socket
import threading
from zipfile import ZipFile
from django.utils.crypto import get_random_string #POSTERIORMENTE CAMBIAR A CADENA GENERADA POR NOSOTROS
import hashlib
from config import Config
import subprocess
from datetime import datetime

from flask import render_template
from forms import contract_form

import db_manager

app = Flask(__name__)
app.config.from_object(Config)

DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
API_NAME = os.environ['SERVICE_NAME']
DB_DATABASE = os.environ['DB_DATABASE']
HOST_IP = os.environ['HOST_IP']
HOST_PORT = os.environ['HOST_PORT']

ip_blockchain = '148.247.201.227'

id_organization = ""

data_manager = db_manager.db_manager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)

time_register = {}
time_register_sc = {}

contract_folder_in = ""
contract_folder_out = ""


def get_timestamp():
    datetimeObj = datetime.now()
    timeStampStr = datetimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
    return timeStampStr

def createCatalogs(catalog):
	try:
		os.makedirs('./catalogs/' + catalog)
	except OSError as e:
		print(str(e))

def createCatalogDaemon(catalog):
	try:
		os.makedirs(catalog)
	except OSError as e:
		print(str(e))

@app.route('/')
def home():
	h = {'api_name':API_NAME}
	return jsonify(h),200

@app.route('/insert_building_block', methods=['POST'])
def insert_building_block():
	params = request.json
	name_b = params['name_b']
	address_b = params['address_b']
	port = params['port']
	description_text = params['description_text']
	id = params['identification']
	#id = get_random_string(length=80)
	result = data_manager.insert_building_block(id, name_b, address_b, port, description_text)
	return jsonify(result),200

@app.route('/insert_company', methods=['POST'])
def insert_company():
	global id_organization
	params = request.json
	#id = get_random_string(length=80)
	id = params['identification']
	name_c = params['name_c']
	id_organization = name_c
	email = params['email']
	password_c = params['password_c']
	address_c = params['address_c']
	port = params['port']
	result = data_manager.insert_company(id, name_c, email, password_c, address_c, port)
	return jsonify(result),200

def create_value_chain_bb_register(ident, valid_contract, transaction_id, building_block_id, catalog_out):
	vc_id = get_random_string(length=80)
	contract_id = ident
	result = 0
	try:
		building_block_address_data = data_manager.get_bb_address_data(building_block_id)
		print(building_block_address_data)
		print("address data bb" + str(building_block_address_data))
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		data2send = {'vc_id':vc_id, 'contract_id':contract_id, 'valid_contract':str(valid_contract),
					'transaction_id':transaction_id, 'sc_catalog_out':catalog_out, 'sc_ip':HOST_IP, 'sc_port':HOST_PORT}
		url = "http://" + str(building_block_address_data[0]) + ":" + str(building_block_address_data[1]) + "/add_value_chain"
		r = requests.post(url=url, json=data2send, headers=headers)

		result = r.text

		if(result):
			print("CONNECTION SUCESSFULLY [SC-BB]: The connection has been created")
		else:
			print("ERROR [Connection SC-BB]: The connection between the SC manager and the BB manager has failed, please check the logs files")
			result = 0
	except:
		print("Error [Connection-BB]: Connection with building block has failed")
	return result

def insert_daemon_in_sc(catalog_in, building_block_id, transaction_id, id_supply_chain, catalog_in_bb):
	createCatalogDaemon('./DaemonOutputs')
	building_block_address_data = data_manager.get_bb_address_data(building_block_id)
	sentence = "nohup python -u content_daemon_d.py " + str(building_block_address_data[0]) + " ./catalogs/" + catalog_in + " \
					" + str(building_block_address_data[1]) + " 1 " + transaction_id + " " + "In_process" + " push " + DB_USER + " " + DB_PASSWORD + " \
					" + DB_HOST + " " + DB_PORT + " " + DB_DATABASE + " " + catalog_in_bb + " > ./DaemonOutputs/content_daemon_bb_" + str(building_block_id) + "_" + str(id_supply_chain) + " &"
	print(sentence)
	os.system(sentence)


@app.route('/add_contract_sc', methods=['POST'])
def add_contract_sc():
	global contract_folder_in
	global contract_folder_out
	params = request.json
	ident = params['ident']
	name_sc = params['name_sc']
	address_sc = params['address_sc']
	port = params['port']
	valid_contract = '1'
	transaction_id = params['transaction_id']
	building_block_id = params['building_block_id']
	id_supply_chain = params['id_supply_chain']
	try:
		result = data_manager.insert_contract_sc(ident, 'server', name_sc, address_sc, port, valid_contract, transaction_id, building_block_id)
		catalog_in = get_random_string(length = 40)
		catalog_out = get_random_string(length=40)
		createCatalogs(catalog_in)
		#colocar demonio 
		createCatalogs(catalog_out)
		resulto = data_manager.insert_supply_chain(id_supply_chain, ident, catalog_in, catalog_out)

		catalog_out = os.getcwd() + "/catalogs/" + catalog_out  

		print("CHECK 1: " + str(resulto))
		vc_result = create_value_chain_bb_register(ident, valid_contract, transaction_id, building_block_id, catalog_out)
		print("CHECK 3: " + vc_result)
		if(result and int(resulto) and vc_result):
			#colocar demonio en carpeta de entrada de la supply chain
			insert_daemon_in_sc(catalog_in, building_block_id, transaction_id, id_supply_chain, vc_result)

			print('\033[92m' + "Input Folder of SC is: " + catalog_in + '\033[0m')
			print('\033[92m' + "Output Folder of SC is: " + catalog_out + '\033[0m')

			contract_folder_in = catalog_in
			out_elements = catalog_out.split("/")
			contract_folder_out = out_elements[len(out_elements)-1]

			h = {'in':contract_folder_in, 'out':contract_folder_out}
			return jsonify(h),200

			#return str(result)
		else:
			return str(0)
	except:
		return str(0)

@app.route('/add_orders', methods=['POST'])
def add_orders():
	global time_register
	global intermediate
	params = request.json
	print(params)
	id = params['id_order']
	status_o = params['status_o']
	transaction_id = params['transaction_id']
	content_id = params['content_id']
	logistic = params['logistic']
	file_name = params['file_name']
	iden = params['iden']
	#time_register[iden] = {iden:{'start':time.time(), 'transaction_id':transaction_id, 'final':0, 'time':0}}
	if transaction_id in time_register_sc:
		time_register_sc[transaction_id].update({iden:{'start':time.time(), 'transaction_id':transaction_id, 'final':0, 'time':0, 'time_in_bc':0}})
	else:
		time_register_sc[transaction_id] = {iden:{'start':time.time(), 'transaction_id':transaction_id, 'final':0, 'time':0, 'time_in_bc':0}}
	print("The file name is: " + file_name)
	result = data_manager.insert_orders(id, status_o, transaction_id, content_id, logistic, file_name, iden)
	return jsonify(result),200


@app.route('/get_images_bc', methods=['POST'])
def get_images_bc():
	portBC = int(HOST_PORT) + 2
	headers = {'Content-type': 'application/json'}
	data2send = {'id':'NO'}
	url = "http://" + ip_blockchain + ":" + str(portBC) + "/getAllImages"
	r = requests.post(url=url, json=data2send, headers=headers)
	print(str(r.text))
	return jsonify(r.json()),200


@app.route('/get_history_bc', methods=['POST'])
def get_history_bc():
	params = request.json
	id = params['id']
	portBC = int(HOST_PORT) + 2
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'id':id}
	url = "http://" + ip_blockchain + ":" + str(portBC) + "/getHistory"
	r = requests.post(url=url, json=data2send, headers=headers)
	print(str(r.text))
	return jsonify(r.json()),200

@app.route('/get_image', methods=['POST'])
def get_image():
	params = request.json
	id = params['id']
	portBC = int(HOST_PORT) + 2
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'id':id}
	url = "http://" + ip_blockchain + ":" + str(portBC) + "/getImage"
	r = requests.post(url=url, json=data2send, headers=headers)
	print(str(r.text))
	return jsonify(r.json()),200

def get_image_verifiability(id):
	portBC = int(HOST_PORT) + 2
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'id':id}
	url = "http://" + ip_blockchain + ":" + str(portBC) + "/getImage"
	r = requests.post(url=url, json=data2send, headers=headers)
	return str(r.text)



def updateImageinBC(iden, level, transaction_id, content_id, status, newPrevious_hash, newActual_hash, newTimestamp):
	initial_time_bc = time.time()
	portBC = int(HOST_PORT) + 2
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'id':iden, 'newO':id_organization, 'newL':level, 'newBbDes':'Processing Finished', 'newTranId':transaction_id, 'newConId':content_id, 'newS':status, 'newPrevious_hash':newPrevious_hash, 'newActual_hash':newActual_hash, 'newTimestamp':newTimestamp}
	url = "http://" + ip_blockchain + ":" + str(portBC) + "/changeOwner"
	r = requests.post(url=url, json=data2send, headers=headers)
	print(str(r.text))
	time_register_sc[transaction_id][iden]['time_in_bc'] = time.time() - initial_time_bc

def get_transaction(id_order):
    iden_elements = data_manager.get_transaction(id_order)
    iden = list(iden_elements)[0]
    return iden

def get_content_id(id_order):
	iden_elements = data_manager.get_content_id(id_order)
	iden = list(iden_elements)[0]
	return iden

@app.route('/update_orders', methods=['POST'])
def update_orders():
	global time_register_sc
	params = request.json
	status_o = params['status_o']
	id_order = params['id_order']
	iden = params['iden']
	newPrevious_hash = params['newPrevious_hash']
	newActual_hash = params['newActual_hash']
	newTimestamp = get_timestamp()

	transaction_id = get_transaction(id_order)

	time_register_sc[transaction_id][iden]['final'] = time.time()
	time_register_sc[transaction_id][iden]['time'] = time_register_sc[transaction_id][iden]['final'] - time_register_sc[transaction_id][iden]['start']

	print(time_register_sc[transaction_id][iden]['final'])
	print(time_register_sc[transaction_id][iden]['time'])
	
	try:
		result = data_manager.update_order_status(id_order, status_o)
		updateImageinBC(iden, 'Supply chain', get_transaction(id_order), status_o, 'Processed on the organization', newPrevious_hash, newActual_hash, newTimestamp)
		
	except:
		print("Couldn't update product on blockchain network")
		result = {'result': 'without the update'}
	return jsonify(result),200

def get_verifiability_times(chain, verifiability_times):
	print(verifiability_times)
	try:
		new_file = open('./tiempos/verifiability/tiempos/verifiabilityTimes_' + str(chain) + '.csv', "w")
		for i in verifiability_times:
			new_file.write(i + ", " + str(verifiability_times[i]['time']) + "\n")
		new_file.close()
	except:
		print('Error al crear el archivo: ' + './tiempos/verifiability/tiempos/verifiabilityTimes_' + str(chain) + '.csv')

@app.route('/get_verifiability', methods=['POST'])
def get_verifiability():
	print("In the verifiability times")
	for i in time_register_sc:
		print("Verifying: " + str(i))
		try:
			os.makedirs('./tiempos/verifiability/proof/')
			os.makedirs('./tiempos/verifiability/tiempos/')
		except OSError as e:
			print(str(e))
		
		verifiability_times = {}

		try:
			new_file = open("./tiempos/verifiability/proof/verifiabilityProof_" + str(i) + ".txt", "w")
			for j in time_register_sc[i]:
				start_time_verifiability = time.time()
				result = get_image_verifiability(j)
				final_time_verifiability = time.time() - start_time_verifiability
				verifiability_times[j] = {'time':final_time_verifiability}
				new_file.write("\t\t\t\t\t" + str(j) + "\n")
				new_file.write(result + "\n----------------------------------------------------------------")
			new_file.close()
		except:
			print("Error en la creación del archivo de verificabilidad: " + "./tiempos/verifiability/proof/verifiabilityProof_" + str(i) + ".txt")
		
		get_verifiability_times(i, verifiability_times)
	print("get_verifiability_end")
	return jsonify({'result':'finished'}),200

def get_time_register_transaction_id(transaction_ident):
	try:
		new_file = open('./tiempos/sc_tiempos_'+ transaction_ident + ".csv", "w")
		#print(transaction_id_register)
		for i in time_register_sc[transaction_ident]:
			print(i)
			new_file.write(i + "," + str(time_register_sc[transaction_ident][i]['start']) + ", " + str(time_register_sc[transaction_ident][i]['final']) + ", " + str(time_register_sc[transaction_ident][i]['time']) + ", " + str(time_register_sc[transaction_ident][i]['time_in_bc']) + ", " + time_register_sc[transaction_ident][i]['transaction_id'] + "\n")
		new_file.close()
		result = {'result':'file sc_datos_tiempos created at the container folder'}
	except:
		print("Error en la creación de archivo sc_tiempos_" + transaction_ident + ".csv")


@app.route('/get_time_register', methods=['POST'])
def get_time_register():
	try:
		os.makedirs('./tiempos/')
	except OSError as e:
		print(str(e))
	try:
		for i in time_register_sc:
			print(i)
			get_time_register_transaction_id(i)
		result = {'result':' All file sc_datos_tiempos created at the container folder'}
	except:
		print("Error en la creación de archivo sc_datos_tiempos.csv")
	return jsonify(result),200


@app.route('/add_supply_chain', methods=['POST'])
def add_supply_chain():
	params = request.json
	id = get_random_string(length=80)
	creation_date = params['creation_date']
	contract_id = params['contract_id']
	catalog_in = params['catalog_in']
	catalog_out = params['catalog_out']
	result = data_manager.insert_supply_chain(id, contract_id, catalog_in, catalog_out)
	return jsonify(result),200

@app.route('/f', methods=['POST'])
def f():
	"""
	Temporal method to test the transaction_authentication
	"""
	params = request.json
	transaction_id = params['transaction_id']
	result = data_manager.transaction_authentication(transaction_id)
	return jsonify(result),200

@app.route('/test', methods=['POST'])
def test():
	"""
	Temporal method to test the transaction_authentication
	"""
	params = request.json
	transaction_id = params['id']
	print(transaction_id)
	#result = data_manager.transaction_authentication(transaction_id)
	return jsonify(result),200

@app.route('/request_contract', methods=['POST'])
def request_contract():
	ip = request.form['ip']
	port = request.form['port']
	building_block_id = request.form['bb_id']
	raw = request.form.get('remember_me', False)
	ident = get_random_string(length=80)
	name_sc = 'testing'
	address_sc = HOST_IP
	my_port = HOST_PORT
	transaction_id = get_random_string(length=80)

	if(raw):
		print("YES EN EL RAW")
		raw = 1
	else:
		print("NO EN EL RAW")
		raw = 0

	id_supply_chain = get_random_string(length=80)
	output_folder_path = request.form['folder_path']

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'ident':ident, 'name_sc':name_sc, 'address_sc':address_sc, 'port':my_port, 'transaction_id':transaction_id, 
				'building_block_id':building_block_id, 'id_supply_chain': id_supply_chain}
	url = "http://" + str(ip) + ":" + str(port) + "/add_contract_sc"
	r = requests.post(url=url, json=data2send, headers=headers)

	if(r.text != '0'):
		result = data_manager.insert_contract_sc(ident, 'client', name_sc, ip, port, '1', transaction_id, building_block_id)
		resultd = data_manager.insert_supply_chain(id_supply_chain, ident, "", output_folder_path)
		createCatalogDaemon('./DaemonOutputs')
		sentence = "nohup python -u orderSenderDaemon.py " + str(ip) + " ./catalogs/" + output_folder_path + " " + str(port) + " 4 " + transaction_id + " " + "PROCESSED" + " push " + str(raw) + " " + DB_USER + " " + DB_PASSWORD + " \
					" + str(DB_HOST) + " " + str(DB_PORT) + " " + DB_DATABASE + " " + id_organization + " " + building_block_id + " " + str(HOST_PORT) + " > ./DaemonOutputs/orderDaemon_" + id_supply_chain + "_" + output_folder_path + " &"
		os.system(sentence)

		print('\033[92m' + "Output Folder of SC is: " + output_folder_path + '\033[0m')

		return "Request Sent, contract id: " + str(r.text)
	else:
		return "SOMETHING WENT WRONG, try again!"

@app.route('/request_contract_curl', methods=['POST'])
def request_contract_curl():
	params = request.json
	ip = params['ip']
	port = params['port']
	building_block_id = params['bb_id']
	raw = params['remember_me']
	ident = get_random_string(length=80)
	name_sc = 'testing'
	address_sc = HOST_IP
	my_port = HOST_PORT
	transaction_id = get_random_string(length=80)

	if(raw=="True"):
		print("YES EN EL RAW")
		raw = 1
	else:
		print("NO EN EL RAW")
		raw = 0

	id_supply_chain = get_random_string(length=80)
	output_folder_path = params['folder_path']

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	data2send = {'ident':ident, 'name_sc':name_sc, 'address_sc':address_sc, 'port':my_port, 'transaction_id':transaction_id, 
				'building_block_id':building_block_id, 'id_supply_chain': id_supply_chain}
	url = "http://" + str(ip) + ":" + str(port) + "/add_contract_sc"
	r = requests.post(url=url, json=data2send, headers=headers)
	#print(r.text)

	if(r.text != '0'):
		result = data_manager.insert_contract_sc(ident, 'client', name_sc, ip, port, '1', transaction_id, building_block_id)
		resultd = data_manager.insert_supply_chain(id_supply_chain, ident, "", output_folder_path)
		createCatalogDaemon('./DaemonOutputs')
		sentence = "nohup python -u orderSenderDaemon.py " + str(ip) + " ./catalogs/" + output_folder_path + " " + str(port) + " 4 " + transaction_id + " " + "PROCESSED" + " push " + str(raw) + " " + DB_USER + " " + DB_PASSWORD + " \
					" + str(DB_HOST) + " " + str(DB_PORT) + " " + DB_DATABASE + " " + id_organization + " " + building_block_id + " " + str(HOST_PORT) + " > ./DaemonOutputs/orderDaemon_" + id_supply_chain + "_" + output_folder_path + " &"
		os.system(sentence)

		print('\033[92m' + "Output Folder of SC is: " + output_folder_path + '\033[0m')

		#h = {'in':contract_folder_in, 'out':contract_folder_out}
		return jsonify(r.json()),200
		#return "Request Sent, contract id: " + str(r.text)
	else:
		return "SOMETHING WENT WRONG, try again!"



@app.route('/insertNohupSkycdsUpload', methods=['POST'])
def insertNohupSkycdsUpload():
	params = request.json
	tokenuser = params['tokenuser']
	apikey = params['apikey']
	organization = params['organization']
	accessToken = params['accessToken']
	interval = params['interval']
	catalogToken = params['catalogToken']
	folder_path = params['folder_path']

	try:
		sentence = "./skyCDSDaemonExecute.sh " + tokenuser + " " + apikey + " " + catalogToken + " /home/catalogs/" + folder_path + " " + organization + " " + accessToken + " " + str(interval)
		print(sentence)
		os.system(sentence)
		return jsonify({'result':'Daemon is running ' + folder_path})
	except:
		return "SOMETHING WENT WRONG, try again! " + sentence


@app.route('/insertNohupSkycdsDownload', methods=['POST'])
def insertNohupSkycdsDownload():
	params = request.json
	tokenuser = params['tokenuser']
	apikey = params['apikey']
	organization = params['organization']
	accessToken = params['accessToken']
	interval = params['interval']
	catalogToken = params['catalogToken']
	folder_path = params['folder_path']
	skycds_server_ip = params['server_skycds_ip']

	try:
		sentence = "./skyCDSDaemonExecuteDownload.sh " + tokenuser + " " + apikey + " " + catalogToken + " /home/catalogs/" + folder_path + " " + organization + " " + accessToken + " " + str(interval) + " " + skycds_server_ip
		print(sentence)
		os.system(sentence)
		return jsonify({'result':'Daemon is running ' + folder_path})
	except:
		return "SOMETHING WENT WRONG, try again! " + sentence

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
		os.system("rm -r ./Salida/*")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete Salida")

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

	try:
		os.system("rm ./nohup.out")
		os.system("rm ./SkyCDS/nohup.out")
		counter = counter + 1
	except:
		print("Something went wrong while trying to delete nohup.out")

	if(counter > 0):
		return "Something was deleted"
	else:
		return "Nothing was deleted"



@app.route('/traceability')
def traceability():
	return render_template('Timeline/index.html'), 200

@app.route('/verifiability')
def verifiability():
	return render_template('Verification/index.html'), 200

@app.route('/contract_deal')
def contract_deal():
	form = contract_form()
	return render_template('contract.html', title='Make a deal', form=form)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000,debug = True)