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

tokensbb = {'1':'NW1yOJ4utw3Abe6wgDHiqCz5FX2vZzgnzqjzAacBPtNXfCpzO5xBbpfJ24dqn1yHYZAt4pDI6PTYsWTO'}
tokensbb.update({'2':'6756W7FndFa2U5xgOzbCpH1vUEE0qv2c76K6Z2omSVIJfyZ4iZy8cu2sBzCDpaeY3OtS1igYTnyGhJgl'})
tokensbb.update({'3':'EA8tVOkFTDoabgC4pXUmmIjv0mo3Y6TNS5uS94dHh2L0iMm9ZdVPEAq0S9szNVPUtSlOnSsDlxzEGNvR'})
tokensbb.update({'4':'yGNC18rtkEBjEe9wANO9aWKOfGT1UL2IG7UPjBooz6Dobumzg8ma0wofEFUtWiQyhegBZAX6DpmFMVbP'})





tokenuser = "a7e72986fccedad2b1410330f5e992170014ca844103aa16f5de9e3c3eb4c175"
apikey = "bae0d278abd47018db633749bf3a9dc7b275aa0a"
organization = "MOGUI"
accessToken = "cec5f56066d556b128d9c8749fb0ca1678d5e79f3587182f08425dbe8285d92a"
interval = "30"
server_skycds_ip = "148.247.201.227"


catalogToken = []
catalogToken.append(['2cdcd954ab1813595092e02c6f898cc06b3d6834a4a0451ce9ea97c19684d899', '39e7029696a82849491f63beda96f65e4587d86d9a009fe4d7560a623fdc41ba', '2b61868a63c009c01d04773f3167ff30ac8a54d9f719a23cfa8368d3537e922f'])
catalogToken.append(['08048c123cb5b52d7966e17a8d2b26502c796bee546262938e0f2dfc8ec64d8f', 'dd2f6d9cb35af46f1f760ea294bbc6fc5a4dd70887f5f0f76f59b67c8f15725c', '96907f0b6812e4d173e99f917798446d9be8fb8357c534c079b0a592bbed0135'])
catalogToken.append(['7aba845fd3442d477df57977bf8f1640322807bfdcc6d423b72cecb49bbaa15e', 'e94f3098b763860db1f830e83e4a99bba55f37030968489ced3fe8524c6dd2ab', '63f41a2e46da0485c594600605f151aa927c89b4d500257dc67d8abf66feef8b'])
catalogToken.append(['438402a1907f1f0233be410b6a0d97222e35da544a090a5421a973aa3a231ef5', 'd2c9b657be43050d85a21c513737cccf43593f98352e12b630a26b45cbd6dc2d', '8921f9a5c4c241e1dc1777a500ca84c7f1ca90a9eb7e2b07f7238d3583d56c2b'])
catalogToken.append(['91eefa20e6bd814691e43eaebf17f0bc74db4965f7e40273d8c71282b64f9866', 'a963c6247d9422cb39f85cac8cec538ce729d24ddcf49d61495fcd0d7796e524', '0264b46901b0e35fb76b78543a2aa869fd090a02cc1180f0c4b3d7ecc0cee420'])
catalogToken.append(['5193979513d9c05dbb6b19177fecc3377c2b8281f918ad53b8b0a2bf4b6e5520', '0e9c96c25d0f3c6f81384654c876f4882388f3736ae54b51d0d4147d13c5e32b', '81c8eb0b930f9e04f5485a013728254bacebfd73076496fde141213abc245c02'])
catalogToken.append(['8dc5af4eaefc3a61978940c4a272198791cb61d3392f7813a29b2b1940f04072', '76e23b67e69280b4a9a7b28033822b78bf2ef62fbd158e0a945f99c60f1574ed', '57a7aa5bacfffee0dda96797bb58b3fbc90997f677677467c6bebaf18d7a53e9'])
catalogToken.append(['4029a4507c4060329216245608892b37f59d0c4691526a6df5fce6d162ed47d1', '08d823548bd2c9e755238ff6e08e3f6a252c71e6c093cceb6e32a838798a65a3', 'ee4d4797b38f7727301e011eae445eb10a46cd0ffc342241ff43e167bbeb2e53'])
catalogToken.append(['437d406d4aa4cfc09157ee49d2c1468f2c8fc7d5eb081303f58d327e29e2b6ca', '3b158b07f9070b304f6531e064a08aa33ed3f93921bf25b9d5d1d05a94884cf4', '1d3af07c48ef7aa0d49a1b31f862c6cefc11eef395e921132d01ebc50fbeb65f'])
catalogToken.append(['110c8bf836e59f8aec0b0be8ca1ce3a3de9ecb888d1109310487e24d9394c859', '2f008604e9b382fea6a1f304839217fe420ba6e8e1f689ed928bdc6563242966', '69a849627860acf9f3abde934ca374fbb689c09169b1676f947a8e6044e5477f'])

for i in range(1,11):
    #----------------------ORG1------------------------
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'ip':ip, 'port':'8005', 'bb_id':tokensbb['2'], 'remember_me':'True', 'folder_path':'cc'+str(i)}
    url = "http://" + sc_managers_ip['1']  + "/request_contract_curl"
    r = requests.post(url=url, json=data2send, headers=headers)
    result = r.json()


    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][0], 'folder_path':'cc'+str(i)}
    url = "http://" + sc_managers_ip['1']  + "/insertNohupSkycdsUpload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)
    print("Carpetas etapa 2: " + result['in'] + "\t" + result['out'])

    #----------------------ORG2------------------------
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][0], 'folder_path':result['in'], 'server_skycds_ip':server_skycds_ip}
    url = "http://" + sc_managers_ip['2']  + "/insertNohupSkycdsDownload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][1], 'folder_path':result['out']}
    url = "http://" + sc_managers_ip['2']  + "/insertNohupSkycdsUpload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'ip':ip, 'port':'8010', 'bb_id':tokensbb['3'], 'remember_me':'False', 'folder_path':result['out']}
    url = "http://" + sc_managers_ip['2']  + "/request_contract_curl"
    r = requests.post(url=url, json=data2send, headers=headers)
    result = r.json()

    print("Carpetas etapa 3: " + result['in'] + "\t" + result['out'])

    #----------------------ORG3------------------------
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][1], 'folder_path':result['in'], 'server_skycds_ip':server_skycds_ip}
    url = "http://" + sc_managers_ip['3']  + "/insertNohupSkycdsDownload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][2], 'folder_path':result['out']}
    url = "http://" + sc_managers_ip['3']  + "/insertNohupSkycdsUpload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)


    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'ip':ip, 'port':'8015', 'bb_id':tokensbb['4'], 'remember_me':'False', 'folder_path':result['out']}
    url = "http://" + sc_managers_ip['3']  + "/request_contract_curl"
    r = requests.post(url=url, json=data2send, headers=headers)
    result = r.json()

    print("Carpetas etapa 4: " + result['in'] + "\t" + result['out'])

    #----------------------ORG4------------------------
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][2], 'folder_path':result['in'], 'server_skycds_ip':server_skycds_ip}
    url = "http://" + sc_managers_ip['4']  + "/insertNohupSkycdsDownload"
    r = requests.post(url=url, json=data2send, headers=headers)
    resultNohup = r.text

    print(resultNohup)
