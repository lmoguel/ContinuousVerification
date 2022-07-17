import time
from datetime import datetime
import sys
import argparse
import multiprocessing


def execute(sensor):
    line = "%s %f PR840 PS%s D "
    sensor = int(sensor)

    i = 1
    j = 1
    f=open("trazas/sensor%d.txt" % sensor, "w")
    f2=open("data/ecg_data_5.csv", "r")
    data = f2.readlines()
    f.close()
    buffer = ""
    
    
    while True:
        d = data[i-1:i+9]
        l = line
        for x in d:
            n = x.split(",")[1].rstrip()
            l += n + " "
            #print(l)

        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%H:%M:%S.%f")
        #print('{:04x}'.format(i))
        buffer += (l+"\n") % (timestampStr,sensor,'{:04x}'.format(j))
        if (i-1)%100 == 0:
            print("Writing")
            f=open("trazas/sensor%d.txt" % sensor, "a")
            f.write(buffer)
            f.close()
            buffer = ""
            time.sleep(2)
        i+=10
        j+=1
        print(len(data), i)
        if i > len(data): break
        
    f2.close()


parser = argparse.ArgumentParser()
parser.add_argument("--sensors", "-s", help="number of sensors", required=True)

args = parser.parse_args()

sensors = int(args.sensors)

print(sensors)

for i in range(sensors):
    t = multiprocessing.Process(target=execute, args=(str(i)))
    t.start()
