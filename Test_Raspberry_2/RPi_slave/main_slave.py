#!/usr/bin/env python

import struct
import os
import can
import socket

from com_slave import *

import VarBerlin_slave as VBS


# *********************************************************
# Connection to bus interface
# *********************************************************
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('Connected to bus can')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

# *********************************************************
# IP addresses configuration
# *********************************************************
IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
IpPink, MACAddr = IpPink.split(' ') # remove MAC address appended
if IpPink == '10.105.0.53': # IOT network
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    IpBlack = '192.168.137.27'
elif IpPink == '192.168.1.21': # Grenier network
    IpBlack = '192.168.1.20'


print('IpBlack - ' + IpBlack)
print('IpPink - ' + IpPink)

# *********************************************************
# Awaiting connection from black car
# *********************************************************
addr = -1
waiting_connection = False
conn = -1
while not VBS.Connection_ON.is_set():
    if addr == -1 and not waiting_connection:
        waiting_connection = True
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((IpPink,TCP_PORT))
            s.listen()
            print('Pink car ready to receive connection')
            conn, addr = s.accept()
        except socket.error:
            conn.close()
            print('Socket error while receiving connection')

    # Check si l'adresse connectée est bien celle de la voiture noire, si oui commence l'envoi des données
    elif (addr == IpBlack):
        waiting_connection = False
        print('Connected to Berlin car with address' + repr(addr))
        VBS.Connection_ON.set()

    # Si quelqu'un autre que la RPi noire se connecte, le déclare, clôt la connection et se met en attente d'une nouvelle
    elif addr != IpBlack and addr != -1:
        waiting_connection = False
        VBS.Connection_ON.clear()
        print('Connected to unknown device, with address ' + repr(addr))
        print('Closing communication channel')
        conn.close()
        addr = -1

'''        
# starting communication with black car
newcomslave = MyComSlave(IpBlack, IpPink)
newcomslave.start()
'''

# *********************************************************
# Messages transmission threads
# *********************************************************
# starting message threads
newreceiveslave = MyReceiveSlave(bus)
newreceiveslave.start()
newsendslave = MySendSlave(VBS.conn,bus)
newsendslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()