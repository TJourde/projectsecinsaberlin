# Programme de test
# Simulation de l'IHM (executé sur voiture rose) pour vérifier le programme executé sur la voiture noire

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
# Variable utilisé pour représenter l' "état interne" du programme principal
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

        # Traitement des informations reçues
        for cmd in data.split(';'):

        	# Erreur pendant le remorquage
            if etape == 3 and 'STATE:towing_error' in cmd:
                print('Towing error')
                break

            # Arrêt possible du remorquage sur commande
            if etape == 3 and 'STATE:towing' in cmd:
                time.sleep(2)
                message = 'TOW:stop;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass

            # Démarrage du remorquage si l'accrochage est validé
            if etape == 2 and 'STATE:hooking_effective' in cmd:
                etape = 3
                message = 'TOW:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)

            # Demande de vérificaiton de l'accrochage en cas de problème
            if etape == 2 and 'STATE:hookin_uneffective' in cmd:
                print('Please verify hooking')
                time.sleep(2)

            # Démarrage de l'accrochage si la connexion entre les deux voitures est validée
            if etape == 1 and 'CON_PINK:on' in cmd:
                etape = 2
                message = 'HOO:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)

            # Ordonne la connexion entre les deux voitures au début du programme
            if etape == 0 and 'STATE:idle' in cmd:
                etape = 1
                message = 'CON:start;'
                print(message)
                size = stest.send(message.encode())
                if size == 0: pass
                time.sleep(2)


except (BrokenPipeError,KeyboardInterrupt):
    print('BrokenPipeError or KeyboardInterrupt')

stest.close()
print('Exiting test_IHM program')