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

# starting communication with black car
newcomslave = MyComSlave(bus)
newcomslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()