# Agrega tiempos de sensado a dos niveles, general y sensado de validacion
import time
import sys
import os
from os import listdir
from os.path import isfile, isdir
import threading
import hashlib
import requests
from django.utils.crypto import get_random_string #POSTERIORMENTE CAMBIAR A CADENA GENERADA POR NOSOTROS
from datetime import datetime

import db_manager

ip = sys.argv[1] # next ip
folder_in = sys.argv[2] # Folder to check for new products
port = sys.argv[3] # next port
sensing_time = sys.argv[4] #sensing times in seconds
transaction_id = sys.argv[5]
status = sys.argv[6]
logistic = sys.argv[7]
DB_USER = sys.argv[8]
DB_PASSWORD = sys.argv[9]
DB_HOST = sys.argv[10]
DB_PORT = sys.argv[11]
DB_DATABASE = sys.argv[12]
catalog_in_bb = sys.argv[13]

files_in = [] # Files information
processed_files = []
processed_files_hashes = []

ip_blockchain = '148.247.201.227'

time_register = []

undone_files = []

files_in_process = [] # Files in process to run the main program

data_manager = db_manager.db_manager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)

print("The actual sensing folder is: " + folder_in)

def get_timestamp():
    datetimeObj = datetime.now()
    timeStampStr = datetimeObj.strftime("%d-%b-%Y %H:%M:%S.%f")
    return timeStampStr

def createCatalogs(path):
	try:
		os.makedirs(path)
	except OSError as e:
		print(str(e))

def get_hash(file_name):
    hasher = hashlib.sha256()
    with open(file_name, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def save_time_registers():
    try:
        os.makedirs('./tiempos/')
    except OSError as e:
        print(str(e))
        
    try:
        new_file = open('./tiempos/sc_content_arrival_' + transaction_id + '.csv', "w")
        for i in time_register:
            new_file.write(i[0] + ", " + str(i[1]) + ", " + i[2] + "\n")
        new_file.close()
        print('The folder sc_content_arrival_' + transaction_id + '.csv has been created')
    except:
        print("Error en la creación de archivo sc_content_arrival_" + transaction_id + ".csv")

def save_logs_thread():
    fi = folder_in.split("/")
    fout = open('./logs/' + fi[2] + ".txt", 'w')
    fout.write('Processed Files\n______________\n' + str(processed_files))
    fout.write('\n\n\nUndone Files\n______________\n' + str(undone_files))
    fout.write('\n\n\nProcessed Files Hashes\n______________\n' + str(processed_files_hashes))
    fout.close()
    save_time_registers()


def sendOrder(content_id, transaction_id, file_name):
    result = 0
    
    try:
        id_order_elements = data_manager.get_id_order(content_id, transaction_id)
        id_order = list(id_order_elements)[0]
        print("EL ID DE LA ORDEN ES: " + str(id_order))
        #print("EL ID DE LA ORDEN ES: " + list(id_order)[0])
        #id_order = get_random_string(length=80)

        id_iden_elements = data_manager.get_identification(content_id, transaction_id)
        iden = list(id_iden_elements)[0]
        time_register.append([iden, time.time(), transaction_id])

        print("EL iden del producto es: " + str(iden))

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data2send = {'id_order':id_order, 'status_o':"building", 'transaction_id':transaction_id, 'content_id':content_id, 'logistic':logistic, 'file_name':file_name, 'iden':iden}
        url = "http://" + str(ip) + ":" + str(port) + "/add_orders"
        r = requests.post(url=url, json=data2send, headers=headers)
        print(str(r.text))
        result = 1
    except:
        result = 0
    return result

def sendFile(file_name, theHash):
    id_order = data_manager.get_id_order(theHash, transaction_id)
    id_order = list(id_order)[0]
    file_name_elements = file_name.split(".")
    
    c_in = catalog_in_bb.split('/')
    c_in_final = ""
    for i in range(2, len(c_in)):
        c_in_final = c_in_final + "/" + c_in[i]
    
    f_in = folder_in.split("/")
    f_in_final = ""
    for i in range(2,len(f_in)):
        f_in_final = f_in_final + "/" + f_in[i]

    sentence = "cp " + folder_in + "/" + file_name + " ./catalogs" + c_in_final + "/" + id_order + "." + file_name_elements[1]
    print("LA INSTRUCCION DE COPIAR ES: " + sentence)
    os.system(sentence)
    #print(sentence)

def inProcess_thread(file_information):
    print("COMIENZA HILO DE: " + file_information[0])
    global files_in_process
    global processed_files
    global processed_files_hashes
    processed_files
    information_step_1 = []
    information_step_2 = []
    information_step_3 = []
    flag = 1

    while flag:
        time.sleep(1)
        actual_files_in = getFilesInformation(folder_in + "/")
        actual_files_in_name = extractName(actual_files_in)
        new_file_information_index = actual_files_in_name.index(file_information[0])
        #print(str(actual_files_in_name.index(file_information[0])) + " word: " + file_information[0])
        information_step_3 = information_step_2
        information_step_2 = information_step_1
        information_step_1 = actual_files_in[new_file_information_index]

        if(information_step_1 == information_step_2 == information_step_3):
            theHash = get_hash(folder_in + "/" + file_information[0])
            if(theHash not in processed_files_hashes):
                # Execute the main program here
                #print('Nombre: ' + file_information[0])
                flag2Continue = sendOrder(theHash, transaction_id, file_information[0])
                print("El Flag del send Order es: " + str(flag2Continue))
                if(flag2Continue):
                    processed_files.append(information_step_1)
                    files_in_process.pop(files_in_process.index(file_information[0]))
                    processed_files_hashes.append(theHash)
                    print("SEND TO PROCESSING: " + str(information_step_1))
                    sendFile(file_information[0], theHash)
                else:
                    files_in_process.pop(files_in_process.index(file_information[0]))
                    print("No se envio a procesamiento")
            else:
                print("NOT SEND TO PROCESSING, ALREADY PROCESSED BEFORE: " + str(information_step_1))
                undone_files.append(information_step_1)
                files_in_process.pop(files_in_process.index(file_information[0]))
            flag = 0

def extractName(lst): 
	return list(next(zip(*lst)))

def getFilesInformation(path):
    temporal_files_in = []
    try:
        with os.scandir(path) as dir_contents:
            for entry in dir_contents:
                if isfile(entry):
                    info = entry.stat()
                    trf = tuple([entry.name, info.st_mtime, info.st_size])
                    temporal_files_in.append(trf)
        return temporal_files_in
    except:
        print("ERROR [Order Daemon]: Couldn't read the folder")
        return False

writer_counter = 0
limit_writer_counter = 3 # Iterations limit to write logs

createCatalogs('./logs')

while 1:
    print("Entra en while")
    if(writer_counter == limit_writer_counter):
        # Write logs
        th_logs = threading.Thread(target=save_logs_thread)
        th_logs.start()
        writer_counter = 0
    time.sleep(int(sensing_time))
    files_in = getFilesInformation(folder_in + "/")
    if(files_in):
        s = set(processed_files)
        s_undone = set(undone_files)
        new_files = [x for x in files_in if x not in s and x not in s_undone]
        #print(new_files)
        for i in new_files:
            if(i[0] not in files_in_process):
                files_in_process.append(i[0])
                th = threading.Thread(target=inProcess_thread, args=(i,))
                th.start()
        
    #new_files_name = extractName(new_files)
    #print("---------------")
    #for c in new_files:
    #    print(c)
    #print("---------------")
    writer_counter += 1
