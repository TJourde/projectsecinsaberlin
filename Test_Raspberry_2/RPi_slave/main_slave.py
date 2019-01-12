#!/usr/bin/env python

import struct
import os
import can
import socket

from com_slave import *

import VarBerlin_slave as VBS


# Try connection to bus interface
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('Connected to bus can')
except OSError:
    print('Cannot find PiCAN board.')
    exit()


# Search own IP address to know which network it's on
IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
if IpPink == '10.105.0.53': # IOT network
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    IpBlack = '192.168.137.27'
elif IpPink == '192.168.1.21': # Grenier network
    IpBlack = '192.168.1.20'


print('IpBlack - ' + IpBlack)
print('IpPink - ' + IpPink)
# starting communication with black car
newcomslave = MyComSlave(IpBlack, IpPink)
newcomslave.start()

# starting message threads
newreceiveslave = MyReceiveSlave(bus)
newreceiveslave.start()
newsendslave = MySendSlave(bus)
newsendslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()