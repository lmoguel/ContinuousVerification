import os
import sys
from os import listdir
from os.path import isfile, isdir
import time

folder_in = sys.argv[1] # /home/raw_material/10

files_in = [] # Files information
processed_files = []


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
        print("ERROR [Order Daemon]: Couldn't read the folder ")
        return False
    



def fileCopy(file_information):
    global processed_files
    processed_files.append(file_information[0])
    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c1"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c2"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c3"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c4"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c5"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c6"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c7"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c8"
    os.system(sentence)
    
    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c9"
    os.system(sentence)

    sentence = "cp " + folder_in + "/" + file_information[0] + " /home/catalogs/c10"
    os.system(sentence)
    #sentence = "cp " + folder_in + "/" + file_information[0] + " /home/fernando/Escritorio/skyCDS_Junio/f2"
    #os.system(sentence)

files_in = getFilesInformation(folder_in + "/")
if(files_in):
    s = set(processed_files)
    new_files = [x for x in files_in if x not in s]
    #print(new_files)
    for i in new_files:
        print(i[0])
        fileCopy(i)
        time.sleep(1)


#cp /home/raw_material/10/* /home/catalogs/entrada/
#python3 sensado_10_cadenas.py /home/fernando/Escritorio/skyCDS_Junio/f1
