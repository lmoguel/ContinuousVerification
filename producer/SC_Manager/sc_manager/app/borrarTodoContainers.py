import json
import sys
import requests
import time
import os

ip_1 = "148.247.201.171"
ip_2 = "148.247.201.221"
ip_3 = "148.247.201.222"
ip_4 = "148.247.201.223"

sc_managers_ip = {'1':ip_1+':8000'}
sc_managers_ip.update({'2':ip_2+':8005'})
sc_managers_ip.update({'3':ip_3+':8010'})
sc_managers_ip.update({'4':ip_4+':8015'})

bb_ip = {'1':ip_1+':8003'}
bb_ip.update({'2':ip_2+':8008'})
bb_ip.update({'3':ip_3+':8013'})
bb_ip.update({'4':ip_4+':8018'})


for i in range(1,5):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {}
    url = "http://" + sc_managers_ip[str(i)]  + "/deleteAll"
    r = requests.post(url=url, json=data2send, headers=headers)
    print(r.text)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {}
    url = "http://" + bb_ip[str(i)]  + "/deleteAll"
    r = requests.post(url=url, json=data2send, headers=headers)
    print(r.text)
