import time
import sys
import os

tokenuser = sys.argv[1]
apikey = sys.argv[2]
catalogToken = sys.argv[3]
chunk_path = sys.argv[4]
organization = sys.argv[5]
accessToken = sys.argv[6]
interval = sys.argv[7]

while 1:
    print("Sensing the folder (upload): " + chunk_path)
    sentence = "java -jar /home/SkyCDS/Demons_Up.jar " + tokenuser + " " + apikey + " " + catalogToken + " single bob 2 " + chunk_path + " " + organization + " true " + accessToken
    os.system(sentence)
    time.sleep(int(interval))
