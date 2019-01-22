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
BUFFER_SIZE = 1024
etape = 0

try:
    stest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    stest.connect((IpBlack,TCP_PORT))
    print('Conneted to black car as IHM')
    time.sleep(5)

    while 1:
        data = stest.recv(BUFFER_SIZE)
        data = str(data)
        data = data[2:len(data)-1]
        if not data: break

        for cmd in data.split(';'):
            #print(cmd)

            if etape == 3 and 'STATE:towing_error' in cmd:
                print('Towing error')
                break

            if etape == 3 and 'STATE:towing' in cmd:
                time.sleep(2)
                message = 'TOW:stop;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass

            if etape == 2 and 'STATE:hooking_effective' in cmd:
                etape = 3
                message = 'TOW:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)

            if etape == 2 and 'STATE:hookin_uneffective' in cmd:
                print('Please verify hooking')
                time.sleep(2)

            if etape == 1 and 'CON_PINK:on' in cmd:
                etape = 2
                message = 'HOO:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)

            if etape == 0 and 'STATE:idle' in cmd:
                etape = 1
                message = 'CON:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)


except (BrokenPipeError,KeyboardInterrupt):
    print('BrokenPipeError')

stest.close()
print('Exiting test_IHM program')