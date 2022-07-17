import json
import sys
import requests
import time
import os

ip_1 = "192.168.0.4"
ip_2 = "148.247.201.171"
ip_3 = "148.247.201.221"
#ip_4 = "192.168.0.21"

sc_managers_ip = {'1':ip_1+':8015'}
sc_managers_ip.update({'2':ip_2+':8000'})
sc_managers_ip.update({'3':ip_3+':8005'})
#sc_managers_ip.update({'4':ip_4+':8015'})

tokensbb = {'1':'QjLlH666dEBYBjSXDA1aar2OdO0E0KiSrZeXquk2KSSIBpbf9WXPOLAPsd5kn1vaoV9Rlhcrbb5ScNjs'}
tokensbb.update({'2':'VhdYcVtZx7DmaQZj6sg0ykOGfTaWegwBi7dzZCjKssZXW2tmKak4SqhjF5M5jp9pvbCjN7EoTpRP9EDe'})
tokensbb.update({'3':'4PBNDuzilzFdgaDrZPnnNwBWZoaqBTYRoR81IVNZmttYrdPP3YXabG9ohyMamMV51m3XBPc3VWXos9C3'})
#tokensbb.update({'4':'yGNC18rtkEBjEe9wANO9aWKOfGT1UL2IG7UPjBooz6Dobumzg8ma0wofEFUtWiQyhegBZAX6DpmFMVbP'})


tokenuser = "640dc6fb130c1ee60ac7ac42c3c90c9322a20066d18d1f86238ff973e130a568"
apikey = "13174e16c509e12c71586d0d0bf40bf55f304955"
organization = "MOGUI"
accessToken = "44fb6cbc3265aa2657d68a4b01b6ffe6db8c0768261df53250cb40ca0097bfbd"
interval = "8"
server_skycds_ip = "148.247.201.227"

catalogToken = []
catalogToken.append(['4bffd4f8a25efe20077b5d50fe5297553e5c542d90f6a319c90d2c7d65e77cf5', 'e1001bd6ec913bd68335b868b0a38146c76d178515ddf4efbc43761e21426f0b'])
catalogToken.append(['53cf91cc0eb76f8f301eacae6f48ae821824b67c916f981f2bdfee187a3fedcc', '362b0adebc82cd99ae269f57d758093300558cd7164aa61d13dba0b2cd85f327'])
catalogToken.append(['12f27481118e4abbbbb7f7c162494ef60d2679c43f08ef054c96ebc8e79c5ca3', '3caccf93e970ab9e83b57036f64be770bac8baf0e3e7e813ce7dea7666477d56'])
catalogToken.append(['c56dcd6c64d74c424b0aa75b7a36e622d9652e67157488ac0428c6e38e71b202', 'eb46d35738a7fd8ceee40fa17a91454719d8844f4f5b251f91b4a6fe58bf17eb'])
catalogToken.append(['caf3eadc9a567c88c93a7a78734e55f24f82d6b6bd7d8493679e2f80278ffee1', '46ab665177026db47599f7210674cf5b0326cb33871a226bc423cc3f784b0c79'])
catalogToken.append(['4154a74edbdf3ffbcac79fbfed02a75fe0a896a673ae15026e2426dd88285ec8', 'dcc057eb98d68ce208211dbc8837dc7dc187b796acbdbc762f77a9799d14b5ca'])
catalogToken.append(['b4de04be134a2ae6c8a5627389113b6614ac570c4dd46bec2249be2033fc9710', '1e780fe40a84691c4960a0bf9c26a6ca7ac47057d6b243c85017c77ba53c7277'])
catalogToken.append(['14e57100db108ad863519ee7f7a1191c49fa0909945be9eaada43c9292c1258c', '9aae3aeb03883b19941a44002c33d8e731000a4cdaa36e727e730daf070977f7'])
catalogToken.append(['705622013c4caf9ebe914671e8892e66e40faad5af8335f7dd096503e10ad46e', 'c8567617eb8cfba6c1286b6b0e53d9fe551784a3797338d6df35590499ea2e87'])
catalogToken.append(['a679c06b1bb8de116dae711679dfa293bcfe1ebca4fca82a270f0a7fa4f58bb9', '80b0c1a492615fad969bd2de137b543b4f852428c79fa37b735909a95df3b532'])


for i in range(1,11):
    #----------------------ORG1------------------------
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'ip':ip_2, 'port':'8000', 'bb_id':tokensbb['2'], 'remember_me':'True', 'folder_path':'cc'+str(i-1)}
    url = "http://" + sc_managers_ip['1']  + "/request_contract_curl"
    r = requests.post(url=url, json=data2send, headers=headers)
    result = r.json()


    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data2send = {'tokenuser':tokenuser, 'apikey':apikey, 'organization':organization, 'accessToken':accessToken, 'interval':interval, 'catalogToken':catalogToken[i-1][0], 'folder_path':'cc'+str(i-1)}
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
    data2send = {'ip':ip_3, 'port':'8005', 'bb_id':tokensbb['3'], 'remember_me':'False', 'folder_path':result['out']}
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

    
