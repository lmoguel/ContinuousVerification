import time
from datetime import datetime
import sys
import argparse
import multiprocessing
import os

def save_time_registers(sensor, tiempos_generacion):
    try:
        os.makedirs('./tiempos/')
    except OSError as e:
        print(str(e))
        
    try:
        new_file = open('./tiempos/sc_generation_time_' + str(sensor) + '_100.csv', "w")
        for i in tiempos_generacion:
            new_file.write(i + ", " + str(tiempos_generacion[i]['inicio']) + ", " + str(tiempos_generacion[i]['final']) + ", " + str(tiempos_generacion[i]['total']) + "\n")
        new_file.close()
        print('The folder tiempos/sc_generation_time_' + str(sensor) + '.csv has been created')
    except:
        print("Error en la creación de archivo tiempos/sc_generation_time_" + str(sensor) + ".csv")

def execute(sensor):
    line = "%s %f PR840 PS%s D "
    sensor = int(sensor)

    i = 1
    j = 1
    #f=open("trazas/sensor%d.txt" % sensor, "w")
    f2=open("data/ecg_data_5.csv", "r")
    data = f2.readlines()
    #f.close()
    buffer = ""
    
    contador = 0
    
    generation_times = {}
    bandera_guardar = 0
    bandera_tiempo = 0
    contador_files = 0

    while True:
        if(bandera_tiempo == 0):
            start_generation_time = time.time()
            bandera_tiempo = 1
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
        

        if ((i-1)%100 == 0):
            if(bandera_guardar == 4):
                print("Writing")
                f=open("catalogs/cc" + str(sensor) + "/sensor" + str(sensor) + "_" + str(contador) + "_100" + ".txt", "w")
                f.write(buffer)
                f.close()
                contador = contador + 1
                buffer = ""
                time.sleep(10)
                final_generation_time = time.time()
                total_generation_time = final_generation_time - start_generation_time
                generation_times["sensor" + str(sensor) + "_" + str(contador)] = {'inicio':start_generation_time, 'final':final_generation_time, 'total':total_generation_time}
                bandera_tiempo = 0
                bandera_guardar = 0
                save_time_registers(sensor, generation_times)
                contador_files = contador_files + 1
            else:
                bandera_guardar = bandera_guardar + 1
        i+=10
        j+=1
        print(len(data), i)
        if i > len(data): 
            break
        elif(contador_files == 2):
            break
    f2.close()


parser = argparse.ArgumentParser()
parser.add_argument("--sensors", "-s", help="number of sensors", required=True)

args = parser.parse_args()

sensors = int(args.sensors)

print(sensors)

for i in range(sensors):
    t = multiprocessing.Process(target=execute, args=(str(i)))
    t.start()
