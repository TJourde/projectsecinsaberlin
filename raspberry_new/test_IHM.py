# Test de connexion entre voiture noire (client) et voiture rose (serveur)

import socket
import struct
import time
import os


# ***************************
# Configuration de l'adresse IP
# ***************************
global IpBlack
global IpPink

IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
try:
    IpPink, MACAddr = IpPink.split(' ') # remove MAC address appended
except ValueError:
    pass
if IpPink == '10.105.0.53': # IOT network
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    IpBlack = '192.168.137.27'
elif IpPink == '192.168.1.21': # Grenier network
    IpBlack = '192.168.1.20'

print('IpBlack - ' + IpBlack)
print('IpPink - ' + IpPink)


# ***************************
# Creation du socket et connexion
# ***************************
TCP_PORT = 6666
BUFFER_SIZE = 24
try:
    stest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stest.connect((IpBlack,TCP_PORT))
    print('Conneted to black car as IHM')
    time.sleep(5)

    message = 'HOO:start;'
    size = stest.send(message.encode())
    if size == 0: pass

    while 1:
        data = stest.recv(50)
        data = str(data)
        data = data[2:len(data)-1]
        if not data: break
        for cmd in data.split(';')
        	print(data)
except BrokenPipeError:
	stest.close()
	print('Exiting test_IHM program')
	exit()

stest.close()
print('Exiting test_IHM program')