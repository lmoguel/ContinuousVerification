import os
import errno
from django.utils.crypto import get_random_string #POSTERIORMENTE CAMBIAR A CADENA GENERADA POR NOSOTROS
import time
import requests
import sys
configuration = open('./general_configuration.cfg', 'r')

organization = []
buildingBlock = []
stages = []


startFlag = 0 # 1: Organization, 2: Building block, 3: Stages, 0: Ninguno
temporal = []

building_block_array = []
stages_array = []


def temporalSaving(linea, flag):
	global temporal
	n = linea.count('\t')
	if(n == 1):
		if(len(temporal) != 0):
			saveRegister(flag)
		temporal = []
		linea = linea.strip()
		lineSet = linea.split(":")
		temporal.append(lineSet[0])
	else:
		data = []
		linea = linea.strip()
		line = linea.split("=")
		data.append(line[0].strip())
		line = line[1].strip()
		line = line.split(" ")
		for i in line:
			data.append(i)
		temporal.append(data)

def saveRegister(flag):
	global temporal
	global organization
	global buildingBlock
	global stages

	if(flag == 1):
		organization.append(temporal)
		temporal = []
	elif(flag == 2):
		buildingBlock.append(temporal)
		temporal = []
	elif(flag == 3):
		stages.append(temporal)
		temporal = []

def analizeLine(linea):
	global startFlag
	global temporal
	global valueChain
	linea = linea.rstrip('\n')
	if(linea == 'ORGANIZATION' or linea == 'BUILDING_BLOCK'  or linea == 'STAGES'):
		if(linea == 'ORGANIZATION'):
			startFlag = 1
		elif(linea == 'BUILDING_BLOCK'):
			startFlag = 2
		elif(linea == 'STAGES'):
			startFlag = 3
	elif(linea == 'END'):
		saveRegister(startFlag)
		startFlag = 0
	else:
		if(startFlag != 0):
			temporalSaving(linea, startFlag)

def configurationFileReading():
	for linea in configuration.readlines():
		analizeLine(linea)
	configuration.close()

def composeFileCreation():
	sentence = ""
	volumesName = ""

	sentence = "version: '3'"
	sentence = sentence + "\nservices:"
	sentence = sentence + "\n  vcmanager:\n    build:\n      context: ./\n    environment:\n      IP: vcmanager\n      PORT: 5000\n    ports:\n      - '4999:80'\n    volumes:\n      - vcmanager:/home/\n      - ./:/home/\n    tty: true\n    entrypoint: ['python', 'ValueChainManager.py']\n    restart: always\n    depends_on:"

	for i in buildingBlock:
		sentence = sentence + "\n      - " + i[0].lower()
		volumesName = volumesName + "\n  " + i[0].lower() + ":"
	sentence = sentence + "\n    networks:\n      - " + virtualP2P[0][0]

	nodesId = zip(*nodes)
	contador = 0
	for i in buildingBlock:
		firstElementBuildingBlock = zip(*i)[0]
		buildingIndex = firstElementBuildingBlock.index("node")
		nodeIndex = nodesId[0].index(i[buildingIndex][1])
		node = nodes[nodeIndex]
		firstElementNodes = zip(*node)[0]
		ip = node[firstElementNodes.index("ip")][1]
		port =  node[firstElementNodes.index("port")][1]
		buildingIndex = firstElementBuildingBlock.index("folder_path")
		sentence = sentence + "\n  " + i[0].lower() + ":\n    build:\n      context: ./" + i[buildingIndex][1] + "\n    environment:\n      IP: " + ip + "\n      PORT: 5000"
		sentence = sentence + "\n    ports:\n      - '" + str(port) + "'"
		sentence = sentence + "\n    volumes:\n      - " + i[0].lower() + ":/home/"
		sentence = sentence + "\n      - ./HuellaDigital/Nodo" + str(contador) + "/app:/home/"
		sentence = sentence + "\n    tty: true\n    entrypoint: ['python', 'BuildingBlockManager.py']\n    restart: always\n    networks:\n      - " + virtualP2P[0][0]
		contador = contador + 1
	sentence = sentence + "\nnetworks: \n  " + virtualP2P[0][0] + ":"
	sentence = sentence + "\nvolumes: \n  vcmanager:" + volumesName
	fout = open('./SC_Manager/docker-compose.yml', 'w')
	fout.write(sentence)
	fout.close()

def composeSCFileCreation():
	sentence = ""
	volumesName = ""

	port = int(organization[0][5][1])
	ip = organization[0][4][1]

	sentence = "version: '3'\n"
	sentence = sentence + "services:\n"
	sentence = sentence + "  db_sc_" + str(port) + ":\n"
	sentence = sentence + "    image: postgres\n"
	sentence = sentence + "    ports:\n"
	sentence = sentence + "      - " + str(port+1) + ":5432\n"
	sentence = sentence + "    expose:\n"
	sentence = sentence + "      - \"5432\"\n"
	sentence = sentence + "    environment:\n"
	sentence = sentence + "      POSTGRES_DB: sc\n"
	sentence = sentence + "      POSTGRES_USER: postgres\n"
	sentence = sentence + "      POSTGRES_PASSWORD: postgres\n"
	sentence = sentence + "    volumes:\n"
	sentence = sentence + "      - ./database/sc_db.sql:/docker-entrypoint-initdb.d/sc_db.sql\n"
	sentence = sentence + "      - psql-sc:/var/lib/postgresql/data\n"
	sentence = sentence + "    restart: always\n"

	sentence = sentence + "  sc_manager_" + str(port) + ":\n"
	sentence = sentence + "    build:\n"
	sentence = sentence + "      context: ./sc_manager\n"
	sentence = sentence + "    ports:\n"
	sentence = sentence + "      - " + str(port) + ":5000\n"
	sentence = sentence + "    volumes:\n"
	sentence = sentence + "      - catalogs_" + str(port) + ":/home/catalogs/\n"
	sentence = sentence + "      - ./sc_manager/app/:/home/\n" # QUITAR EN PRODUCCION
	#sentence = sentence + "      - ./sc_manager/app/Outputs_Files/:/home/Outputs_Files/\n"
	sentence = sentence + "    environment:\n"
	sentence = sentence + "      SERVICE_NAME: sc\n"
	sentence = sentence + "      DB_HOST: db_sc_" + str(port) + "\n"
	sentence = sentence + "      DB_PORT: 5432\n"
	sentence = sentence + "      DB_USER: postgres\n"
	sentence = sentence + "      DB_PASSWORD: postgres\n"
	sentence = sentence + "      DB_DATABASE: sc\n"
	sentence = sentence + "      HOST_IP: " + ip + "\n"
	sentence = sentence + "      HOST_PORT: " + str(port) + "\n"
	sentence = sentence + "    tty: true\n"
	sentence = sentence + "    command: python supply_chain_manager.py\n"
	sentence = sentence + "    restart: always\n"
	sentence = sentence + "    depends_on:\n"
	sentence = sentence + "      - db_sc_" + str(port) + "\n\n"

	sentence = sentence + "volumes:\n"
	sentence = sentence + "  psql-sc:\n"
	sentence = sentence + "    driver: local\n"
	sentence = sentence + "  catalogs_" + str(port) + ":\n"
	sentence = sentence + "    external:\n"
	sentence = sentence + "      name: volumes_catalogs_" + str(port) 
	fout = open('./SC_Manager/docker-compose.yml', 'w')
	fout.write(sentence)
	fout.close()

def generateSentenceFile(block_name, block_port):
	port = int(organization[0][5][1])
	sentence = "version: '3'\n"
	sentence = sentence + "services:\n"
	sentence = sentence + "  db_" + block_name + "_" + str(port) + ":\n"
	sentence = sentence + "    image: postgres\n"
	sentence = sentence + "    ports:\n"
	sentence = sentence + "      - " + str(block_port+1) + ":5432\n"
	sentence = sentence + "    expose:\n"
	sentence = sentence + "      - \"5432\"\n"
	sentence = sentence + "    environment:\n"
	sentence = sentence + "      POSTGRES_DB: " + block_name + "\n"
	sentence = sentence + "      POSTGRES_USER: postgres\n"
	sentence = sentence + "      POSTGRES_PASSWORD: postgres\n"
	sentence = sentence + "    volumes:\n"
	sentence = sentence + "      - ./database/bb_db.sql:/docker-entrypoint-initdb.d/bb_db.sql\n"
	sentence = sentence + "      - psql-" + block_name + ":/var/lib/postgresql/data\n"
	sentence = sentence + "    restart: always\n"

	sentence = sentence + "  " + block_name + "_manager_" + str(port) + ":\n"
	sentence = sentence + "    build:\n"
	sentence = sentence + "      context: ./bb_manager\n"
	sentence = sentence + "    ports:\n"
	sentence = sentence + "      - " + str(block_port) + ":5000\n"
	sentence = sentence + "    volumes:\n"
	sentence = sentence + "      - catalogs_" + str(port) +  ":/home/catalogs/\n"
	sentence = sentence + "      - ./bb_manager/app/:/home/\n"
	sentence = sentence + "    environment:\n"
	sentence = sentence + "      SERVICE_NAME: " + block_name + "_" + str(port) + "\n"
	sentence = sentence + "      DB_HOST: db_" + block_name + "_" + str(port) + "\n"
	sentence = sentence + "      DB_PORT: 5432\n"
	sentence = sentence + "      DB_USER: postgres\n"
	sentence = sentence + "      DB_PASSWORD: postgres\n"
	sentence = sentence + "      DB_DATABASE: " + block_name + "\n"
	sentence = sentence + "    tty: true\n"
	sentence = sentence + "    command: python building_block_manager.py\n"
	sentence = sentence + "    restart: always\n"
	sentence = sentence + "    depends_on:\n"
	sentence = sentence + "      - db_" + block_name + "_" + str(port) + "\n\n"

	sentence = sentence + "volumes:\n"
	sentence = sentence + "  psql-" + block_name + ":\n"
	sentence = sentence + "    driver: local\n"
	sentence = sentence + "  catalogs_" + str(port) + ":\n"
	sentence = sentence + "    external:\n"
	sentence = sentence + "      name: volumes_catalogs_" + str(port) 

	return sentence

def volume_ymlCreation():
	print(organization)
	port = int(organization[0][5][1])
	sentence = "version: '3'\n\n"
	sentence = sentence + "volumes:\n"
	sentence = sentence + "    catalogs_" + str(port) + ":"
	fout = open('./volumes/docker-compose.yml', 'w')
	fout.write(sentence)
	fout.close()

def createFolderAndCopy(folder_name):
	try:
		os.mkdir(folder_name)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
        try:
		sentence = "cp -r bb_base/* " + folder_name
		os.system(sentence)
	except:
		print("Error al copiar el bb-base")


def composeBBFileCreation(blockInformation):
	createFolderAndCopy(blockInformation['name'])
	sentence = generateSentenceFile(blockInformation['name'].lower(), int(blockInformation['port']))
	fout = open('./' + blockInformation['name'] + '/docker-compose.yml', 'w')
	fout.write(sentence)
	fout.close()


def insert_bb_company():
	print("---------------------------------------------")
	for i in building_block_array:
		result = 0
		try:
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			data2send = {'identification':str(i['id']), 'name_b':i['name'], 'address_b':i['address'],
						'port':i['port'], 'description_text':i['description']}
			url = "http://" + organization_information['address'] + ":" + str(organization_information['port']) + "/insert_building_block"
			#print(url)
			#print(data2send)
			r = requests.post(url=url, json=data2send, headers=headers)

			result = r.text

			if(result):
				print("BUILDING BLOCK COMPANY INFORMATION SAVED, BB: " + i['name'] + "\t" + result)
			else:
				print("ERROR [Company Building Block Information]: " + i['name'])
				result = 0
		except:
			print("Error [Company Building Block Information]: Connection with supply chain manager has failed")

def insert_company():
	print("\n\n\n")
	print("---------------------------------------------")
	print("---------------------------------------------")
	result = 0
	try:
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		data2send = {'identification':str(organization_information['id']), 'name_c':organization_information['name'], 'email':organization_information['email'],
					'password_c':organization_information['password'], 'address_c':organization_information['address'], 'port':organization_information['port']}
		url = "http://" + organization_information['address'] + ":" + str(organization_information['port']) + "/insert_company"
		#print(url)
		#print(data2send)
		r = requests.post(url=url, json=data2send, headers=headers)

		result = r.text

		if(result):
			print("COMPANY INFORMATION SAVED: " + result)
			insert_bb_company()
		else:
			print("ERROR [Company Information]")
			result = 0
	except:
		print("Error [Company Information]: Connection with supply chain manager has failed")

def insert_stages(building_address, building_port, stages_list, building_name):
	for i in stages_list:
		for j in stages_array:
			if(i == j['ident']):
				result = 0
				try:
					headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
					data2send = {'identification':str(j['id']), 'name_s':j['app_name'], 'executable_sentence':j['executable_sentence']}
					url = "http://" + building_address + ":" + str(building_port) + "/insert_stage"
					#print(url)
					#print(data2send)
					r = requests.post(url=url, json=data2send, headers=headers)

					result = r.text

					if(result):
						print("BUILDING BLOCK STAGE INFORMATION SAVED, BB: " + building_name + "\t" + "STG: " + j['ident'] + "\t" + result)
					else:
						print("ERROR [Building Block Stage Information]: " + building_name + "\tSTG: " + j['ident'])
						result = 0
				except:
					print("Error [Building Block Stage Information]: Connection with building block chain manager has failed")

def insert_building_block():
	print("\n\n\n")
	print("---------------------------------------------")
	print("---------------------------------------------")
	time.sleep(4)
	for i in building_block_array:
		result = 0
		try:
			headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
			data2send = {'identification':str(i['id']), 'name_b':i['name'], 'address_b':i['address'],
						'port':i['port']}
			url = "http://" + i['address'] + ":" + str(i['port']) + "/insert_building_block"
			#print(url)
			#print(data2send)
			r = requests.post(url=url, json=data2send, headers=headers)

			result = r.text

			if(result):
				print("BUILDING BLOCK INFORMATION SAVED, BB: " + i['name'] + "\t" + result)
				insert_stages(i['address'], i['port'], i['stages'], i['name'])
			else:
				print("ERROR [Building Block Information]: " + i['name'])
				result = 0
		except:
			print("Error [Building Block Information]: Connection with building block manager has failed")
		print("---------------------------------------------")

def deployProject():
	port = int(organization[0][5][1])
	#sentence = "docker-compose -p nameV_" + str(port) + " -f ./volumes/docker-compose.yml up --build -d"
	sentence = "docker-compose -f ./volumes/docker-compose.yml up --build -d"
	os.system(sentence)
	#sentence = "docker-compose -p sc_manager_" + str(port) + " -f ./SC_Manager/docker-compose.yml up --build -d"
	sentence = "docker-compose -f ./SC_Manager/docker-compose.yml up --build -d"
	os.system(sentence)
	for i in buildingBlock:
		#sentence = "docker-compose -p buil_" + str(port) + "_" + str(i[0]) + " -f ./" + i[0] + "/docker-compose.yml up --build -d"
		sentence = "docker-compose -f ./" + i[0] + "/docker-compose.yml up --build -d"
		os.system(sentence)
	
	#for c in range(0,8):
	#	time.sleep(1)
	#	print("*")
	insert_company()
	insert_building_block()


configurationFileReading()
volume_ymlCreation()
composeSCFileCreation()
#generateCompanyRegister()

for i in buildingBlock:
	blockInformation1 = {}

	for j in range(1, len(i)):
		#print(i[j][1])
		if(i[j][0] != 'stages'):
			blockInformation2 = {i[j][0]:i[j][1]}
			blockInformation1.update(blockInformation2)
		else:
			multiple_array = []
			for k in range(1, len(i[j])):
				multiple_array.append(i[j][k])
			blockInformation2 = {i[j][0]:multiple_array}
			blockInformation1.update(blockInformation2)
	id = get_random_string(length=80)
	blockInformation2 = {'id':id}
	blockInformation1.update(blockInformation2)
	building_block_array.append(blockInformation1)
	composeBBFileCreation(blockInformation1)

for i in stages:
	stagesInformation1 = {}
	stagesInformation2 = {'ident':i[0]}
	stagesInformation1.update(stagesInformation2)
	stagesInformation2 = {'id':get_random_string(length=80)}
	stagesInformation1.update(stagesInformation2)
	for j in range(1, len(i)):
		stagesInformation2 = {i[j][0]:i[j][1]}
		stagesInformation1.update(stagesInformation2)
	stages_array.append(stagesInformation1)


organization_information = {}
for i in range(1, len(organization[0])):
	organization_information2 = {organization[0][i][0]:organization[0][i][1]}
	organization_information.update(organization_information2)
id = get_random_string(length=80)
organization_information2 = {'id':id}
organization_information.update(organization_information2)


print("Please upload the necessary files of your applications (stages) in the following paths:\n")
for i in buildingBlock:
	print("\t./" + i[0] + "/bb_manager/app/DISCH/\n")


print("\n\n\nYou need also to update the following files according to your needs:\n")
for i in buildingBlock:
	print("\t./" + i[0] + "/bb_manager/install-packages.sh\n")
	print("\t./" + i[0] + "/bb_manager/requirements.txt\n")


print("\n\n\nHAVE YOU UPLOADED AND UPDATED THE REQUIRED FILES (Y/N): ?")
answer = raw_input()

if(answer == "Y" or answer == "yes" or answer == "Yes" or answer == "YES" or answer == "y"):
	deployProject()
	#print(building_block_array)
	#print("-------------------")
	#print(stages_array)
	#print("-------------------")
	#print(organization_information)
else:
	print("Try again")


#print(buildingBlock[0])

#print(organization)
#print("------------------------")
#print(buildingBlock)
#print("------------------------")
#(stages)
#print("------------------------")


#os.system("docker-compose up --build")
