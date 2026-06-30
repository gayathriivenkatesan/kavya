import csv
import paramiko
import sys
import json


DeviceName = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

#DeviceName = '10.25.17.33'
#username = 'ro-api-storage'
#password = 'GGNh83wWVZK&EjGC'



def vmValidation(DeviceName, username, password, query):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(DeviceName, username=username, port=22, password=password)
        stdin, stdout, stderr = ssh.exec_command(query)
        output = stdout.read().decode('ascii').strip("\n")
        ssh.close()
        return output
    except Exception as e:
        print(e)
        print("Error: Server Not able to connect. Please try again later...")
        return None

 

query = 'isi status | grep "Cluster Health"'

if DeviceName== '10.25.17.33':
    DeviceHost='DLJDAISILONCLU01'
    
if DeviceName== '10.27.17.166':
    DeviceHost='KCJDAISILONCLU01'

if DeviceName== '10.231.0.151':
    DeviceHost='SL1JDAISILONCLU01'

if DeviceName== '10.233.0.182':
    DeviceHost='FR1JDAISILONCLU01'
    
cluster_status = vmValidation(DeviceName, username, password, query)


if cluster_status is not None and "OK" in cluster_status.upper():
    #print(DeviceName)
    #print(cluster_status)
    DeviceType='Isiolon Devices'
    Remarks='NA'
    status='Healthy'
    IsiolonOutput={'Device':DeviceType,
                   'DeviceName':DeviceHost,
                   'Remark':Remarks,
                   'output_status':status}
    #print(IsiolonOutput)
    output_json = json.dumps(IsiolonOutput)

    print(output_json)
            
else:
            
    #print(DeviceName)
    #print(cluster_status)
    DeviceType='Isiolon Devices'
    Remarks=cluster_status
    #Remarks='Issue Found'
    status='UnHealthy'
    IsiolonOutput={'Device':DeviceType,
                   'DeviceName':DeviceHost,
                   'Remark':Remarks,
                   'output_status':status}

    #print(IsiolonOutput)
    output_json = json.dumps(IsiolonOutput)

    print(output_json)

   
