#!/usr/bin/env python

import struct
import os
import can
import socket

from com_slave import *

global IpPink
global IpBlack
global Connection_ON
global conn

# Search own IP address to know which network it's on
IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
if IpPink == '10.105.0.53': # IOT network
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    IpBlack = '192.168.137.201'

# Try connection to bus interface
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('Connected to bus can')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

# starting communication with black car
newcomslave = MyComSlave()
newcomslave.start()

# starting message threads
newreceiveslave = MyReceiveSlave(conn, bus)
newreceiveslave.start()
newsendslave = MySendSlave(conn, bus)
newsendslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()