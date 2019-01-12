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

print('Black' + VBS.IpBlack)
print('Pink' + VBS.IpPink)
# starting communication with black car
newcomslave = MyComSlave(VBS.IpBlack, VBS.IpPink)
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