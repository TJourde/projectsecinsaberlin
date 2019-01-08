#!/usr/bin/env python

import struct
import os
import can
import socket

from com_slave import *


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
newreceiveslave = MyReceiveSlave(bus)
newreceiveslave.start()
newsendslave = MySendSlave(bus)
newsendslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()