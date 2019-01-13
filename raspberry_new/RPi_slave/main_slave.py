#!/usr/bin/env python

import struct
import os
import can
import socket
import threading

from com_slave import *

import VarBerlin_slave as VBS

# COMMANDES ROUES
NO_MOVE = 0xB1
WHEELS_CENTER = 0xB1

# *********************************************************
# Connection to bus interface
# *********************************************************
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print('Connected to bus can')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

# starting communication with black car
newcomslave = MyComSlave(bus)
newcomslave.start()

time.sleep(5)
msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,0],extended_id=False)
bus.send(msg)

# ending threads
newcomslave.join()
