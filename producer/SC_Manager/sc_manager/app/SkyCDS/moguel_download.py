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
ip = sys.argv[8]

while 1:
    print("Sensing the folder (download): " + chunk_path)
    sentence = "java -jar /home/SkyCDS/RobotDownloader.jar " + tokenuser + " " + apikey + " " + catalogToken + " " + ip + ":20505 2 1 " + organization + " " + chunk_path + " " + accessToken
    os.system(sentence)
    time.sleep(int(interval))
