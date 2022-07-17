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

folder_in = sys.argv[1] # Folder to check for new products
sensing_time = sys.argv[2] #sensing times in seconds
stage_id = sys.argv[3]
stage_name = sys.argv[4]
logistic = sys.argv[5]
folder_out = sys.argv[6]
executable_sentence = sys.argv[7]
DB_USER = sys.argv[8]
DB_PASSWORD = sys.argv[9]
DB_HOST = sys.argv[10]
DB_PORT = sys.argv[11]
DB_DATABASE = sys.argv[12]
type_daemon = sys.argv[13] # 0 intrablock, 1 connection to sc
sc_ip = sys.argv[14]
sc_port = sys.argv[15]
transaction_id = sys.argv[16]


files_in = [] # Files information
processed_files = []
processed_files_hashes = []

ip_blockchain = '148.247.201.227'

undone_files = []

time_register = []

time_register_bb = {}

limit_counter = 10

files_in_process = [] # Files in process to run the main program


data_manager = db_manager.db_manager(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)

"""
We must get stages to control the flow of the transformations
"""
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

def save_time_registers():
    try:
        os.makedirs('./tiempos/' + transaction_id)
    except OSError as e:
        print(str(e))
    
    try:
        stage_name_name = stage_name.split(".")
        stage_name_n = stage_name_name[0]
        new_file = open('./tiempos/' + transaction_id + '/' + stage_name_n  + '.csv', "w")
        for i in time_register_bb:
            new_file.write(i + ", " + str(time_register_bb[i]['time']) + ", " + str(time_register_bb[i]['time_in_bc']) + ", " + time_register_bb[i]['transaction_id'] + "\n")
        new_file.close()
        print('The folder: ' + stage_name_n + '.csv has been created')
    except:
        print('Error en la creación de archivo' + stage_name_n + '.csv')

def get_hash(file_name):
    hasher = hashlib.sha256()
    with open(file_name, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_name():
    iden_elements = data_manager.get_building_name()
    iden = list(iden_elements)[0]
    return iden

def get_previous_hash(iden):
    #start_time_hash = time.time()
    previousHash = "error"
    portBC = int(sc_port) + 2
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'id':iden}
    url = "http://" + ip_blockchain + ":" + str(portBC) + "/getLastHash"
    r = requests.post(url=url, json=data2send, headers=headers).json()
    try:
        previousHash = r[0]['newActual_hash']
    except:
        print("There was something wrong in the get last hash method")
    
    #final_time_hash = time.time() - start_time_hash
    #if iden in time_register_bb:
    #    previous_time_in_bc = time_register_bb[iden]['time_in_bc']
    #    time_register_bb[iden]['time_in_bc'] = previous_time_in_bc + final_time_hash
    #else:
    #    time_register_bb[iden] = {'time':0, 'time_in_bc':final_time_hash, 'transaction_id':transaction_id}

    return previousHash


def updateImageinBC(iden, level, transaction_id, content_id, status):
    try:
        newPrevious_hash = get_previous_hash(iden)
        start_time_update = time.time()
        newActual_hash = content_id
        newTimestamp = get_timestamp()
        portBC = int(sc_port) + 2
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data2send = {'id':iden, 'newO':get_name(), 'newL':level, 'newBbDes':'bb_' + stage_id, 'newTranId':transaction_id, 'newConId':content_id, 'newS':status, 'newPrevious_hash':newPrevious_hash, 'newActual_hash':newActual_hash, 'newTimestamp':newTimestamp}
        url = "http://" + ip_blockchain + ":" + str(portBC) + "/changeOwner"
        r = requests.post(url=url, json=data2send, headers=headers)
        print(str(r.text))

        final_time_hash = time.time() - start_time_update
        if iden in time_register_bb:
            previous_time_in_bc = time_register_bb[iden]['time_in_bc']
            time_register_bb[iden]['time_in_bc'] = previous_time_in_bc + final_time_hash
        else:
            time_register_bb[iden] = {'time':0, 'time_in_bc':final_time_hash, 'transaction_id':transaction_id}


    except:
        print("Couldn't update the product on the blockchain network")


def save_logs_thread():
    fi = folder_in.split("/")
    fout = open('./logs/' + fi[2] + ".txt", 'w')
    fout.write('Processed Files\n______________\n' + str(processed_files))
    fout.write('\n\n\nUndone Files\n______________\n' + str(undone_files))
    fout.write('\n\n\nProcessed Files Hashes\n______________\n' + str(processed_files_hashes))
    fout.close()
    save_time_registers()

def sendOrder(content_id, id_order):
    #id_order = get_random_string(length=80)
    iden = get_iden(id_order)
    newPrevious_hash = 0
    try:
        newPrevious_hash = get_previous_hash(iden)
    except:
        print("Couldn't get the previous hash of the file")
    newActual_hash = content_id
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'id_order':id_order, 'status_o':content_id, 'iden':iden, 'newPrevious_hash':newPrevious_hash, 'newActual_hash':newActual_hash}
    url = "http://" + str(sc_ip) + ":" + str(sc_port) + "/update_orders"
    r = requests.post(url=url, json=data2send, headers=headers)
    print(str(r.text))

def insert_intra_order(content_name, theHash, iden):
    id_intra_order = get_random_string(length=80)
    name_elements = content_name.split(".")
    #id_order = data_manager.get_id_order(theHash)
    result = data_manager.insert_intra_order(id_intra_order, name_elements[0], stage_id, stage_name, theHash, logistic, iden)
    return result

def get_iden(id_order):
    iden_elements = data_manager.get_iden(id_order, transaction_id)
    iden = list(iden_elements)[0]
    return iden

def get_transaction(id_order):
    iden_elements = data_manager.get_transaction(id_order)
    iden = list(iden_elements)[0]
    return iden

def inProcess_thread(file_information):
    #print("COMIENZA HILO DE: " + file_information[0])
    global files_in_process
    global processed_files
    global processed_files_hashes
    processed_files
    information_step_1 = []
    information_step_2 = []
    information_step_3 = []
    flag = 1

    counter = 0

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
                #sendOrder(theHash, transaction_id)
                # Send to order verification method
                iden = get_iden((file_information[0].split("."))[0])
                transaction_id = get_transaction((file_information[0].split("."))[0])
                
                result = insert_intra_order(file_information[0], theHash, iden)
                print("CHECK 1: Result = " + str(result))
                if(result):
                    processed_files.append(information_step_1)
                    files_in_process.pop(files_in_process.index(file_information[0]))
                    processed_files_hashes.append(get_hash(folder_in + "/" + file_information[0]))
                    print("THE PATH IS: " + folder_in + "/" + file_information[0] )
                    print("SEND TO PROCESSING: " + str(information_step_1))
                    sentence = executable_sentence + " ./DISCH/" + stage_name + " " + folder_in + "/" + file_information[0] + " " + folder_out
                    print("THE SENTENCE IS: " + sentence)
                    if iden in time_register_bb:
                        time_register_bb[iden]['time'] = time.time()
                    else:
                        time_register_bb[iden] = {'time':time.time(), 'time_in_bc':0, 'transaction_id':transaction_id}
                    os.system(sentence)

                    updateImageinBC(iden, 'building_block', transaction_id, theHash, stage_name)

                else:
                    print("CHECK 2: No entra en la ejecucion del programa")
            else:
                print("NOT SEND TO PROCESSING: " + str(information_step_1))
                undone_files.append(information_step_1)
                files_in_process.pop(files_in_process.index(file_information[0]))
            flag = 0
        counter = counter + 1
        if(counter == limit_counter):
            files_in_process.pop(files_in_process.index(file_information[0]))
            flag = 0


def inProcess_thread_out(file_information):
    #print("COMIENZA HILO DE: " + file_information[0])
    global files_in_process
    global processed_files
    global processed_files_hashes
    processed_files
    information_step_1 = []
    information_step_2 = []
    information_step_3 = []
    flag = 1

    counter = 0

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
                #sendOrder(theHash, transaction_id)
                # Send to order verification method
                file_name_elements = file_information[0].split(".")
                id_order = file_name_elements[0]

                content_name_elements = data_manager.get_content_name(id_order)
                content_name = list(content_name_elements)[0]

                iden = get_iden((file_information[0].split("."))[0])
                transaction_id = get_transaction((file_information[0].split("."))[0])

                result = data_manager.update_order_status(id_order, 'FINISHED')
                print("CHECK 1: Result = " + str(result))
                if(result):
                    processed_files.append(information_step_1)
                    files_in_process.pop(files_in_process.index(file_information[0]))
                    processed_files_hashes.append(get_hash(folder_in + "/" + file_information[0]))
                    print("THE PATH IS: " + folder_in + "/" + file_information[0] )
                    #print("SEND TO PROCESSING: " + str(information_step_1))
                    #sentence = executable_sentence + " ./DISCH/" + stage_name + " " + folder_in + "/" + file_information[0] + " " + folder_out
                    sendOrder(theHash, id_order)
                    sentence = "cp " + folder_in + "/" + file_information[0] + " " + folder_out + "/" + content_name
                    if iden in time_register_bb:
                        time_register_bb[iden]['time'] = time.time()
                    else:
                        time_register_bb[iden] = {'time':time.time(), 'time_in_bc':0, 'transaction_id':transaction_id}
                    print("THE SENTENCE IS: " + sentence)
                    os.system(sentence)
                    
                    #Borrar a partir de aquí
                    volume_out_elements = folder_out.split("/")
                    volume_out_elements.pop(0)
                    volume_out_elements.pop(0)
                    volume_out_elements.pop(0)

                    volume_sentence = "/home/Outputs_Files/"
                    for k in volume_out_elements:
                        volume_sentence = volume_sentence + k + "/"
                    createCatalogs(volume_sentence)
                    sentence = "cp " + folder_in + "/" + file_information[0] + " " + volume_sentence + content_name
                    print("The sentence to send the final product is; " + sentence)
                    os.system(sentence)

                else:
                    print("CHECK 2: No entra en la ejecucion del programa")
            else:
                print("NOT SEND TO PROCESSING: " + str(information_step_1))
                undone_files.append(information_step_1)
                files_in_process.pop(files_in_process.index(file_information[0]))
            flag = 0
        counter = counter + 1
        if(counter == limit_counter):
            files_in_process.pop(files_in_process.index(file_information[0]))
            flag = 0



def extractName(lst): 
	return list(next(zip(*lst)))

def getFilesInformation(path):
    temporal_files_in = []
    with os.scandir(path) as dir_contents:
        for entry in dir_contents:
            if isfile(entry):
                info = entry.stat()
                trf = tuple([entry.name, info.st_mtime, info.st_size])
                temporal_files_in.append(trf)
    return temporal_files_in

writer_counter = 0
limit_writer_counter = 3 # Iterations limit to write logs

createCatalogs('./logs')


if(type_daemon == '0'):
    while 1:
        print("Entra en while")
        if(writer_counter == limit_writer_counter):
            # Write logs
            th_logs = threading.Thread(target=save_logs_thread)
            th_logs.start()
            writer_counter = 0
        time.sleep(int(sensing_time))
        files_in = getFilesInformation(folder_in + "/")
        s = set(processed_files)
        s_undone = set(undone_files)
        new_files = [x for x in files_in if x not in s and x not in s_undone]
        #print(new_files)
        for i in new_files:
            if(i[0] not in files_in_process):
                files_in_process.append(i[0])
                inProcess_thread(i)
                #th = threading.Thread(target=inProcess_thread, args=(i,))
                #th.start()

        #new_files_name = extractName(new_files)
        #print("---------------")
        #for c in new_files:
        #    print(c)
        #print("---------------")
        writer_counter += 1
else:
    while 1:
        print("Entra en while")
        if(writer_counter == limit_writer_counter):
            th_logs = threading.Thread(target=save_logs_thread)
            th_logs.start()
            writer_counter = 0
        time.sleep(int(sensing_time))
        files_in = getFilesInformation(folder_in + "/")
        s = set(processed_files)
        s_undone = set(undone_files)

        new_files = [x for x in files_in if x not in s and x not in s_undone]
        for i in new_files:
            if(i[0] not in files_in_process):
                files_in_process.append(i[0])
                #th = threading.Thread(target=inProcess_thread_out, args=(i,))
                #th.start()
                inProcess_thread_out(i)

        writer_counter += 1
