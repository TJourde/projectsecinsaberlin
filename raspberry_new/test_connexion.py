# Test de connexion entre voiture noire (client) et voiture rose (serveur)

import socket
import struct
import time
import os


# ***************************
# Configuration de l'adresse IP
# ***************************
IpBlack = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpBlack = IpBlack[:len(IpBlack)-2] #(suppress ' \n')
try:
    IpBlack, MACAddr = IpBlack.split(' ') # remove MAC address appended
except ValueError:
    pass
if IpBlack == '10.105.0.53': # IOT network
    IpPink = '10.105.0.55'
elif IpBlack == '192.168.137.12': # Berlin network
    IpPink = '192.168.137.27'
elif IpBlack == '192.168.1.21': # Grenier network
    IpPink = '192.168.1.20'

print('IpBlack - ' + IpBlack)
print('IpPink - ' + IpPink)


# ***************************
# Creation du socket et connexion
# ***************************
TCP_PORT = 9000
BUFFER_SIZE = 24
stest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stest.connect((IpPink,TCP_PORT))
print('Conneted to pink car')
while 1:
	data = stest.recv(BUFFER_SIZE)
	if not data: break
	print(data)
stest.close()
print('Exiting test program')