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

FindIp()

# starting communication with black car
newcomslave = MyComSlave(IpPink,IpBlack)
newcomslave.start()

# starting message threads
newreceiveslave = MyReceiveSlave(conn,bus)
newreceiveslave.start()
newsendslave = MySendSlave(conn,bus)
newsendslave.start()

# ending threads
newreceiveslave.join()
newsendslave.join()
newcomslave.join()