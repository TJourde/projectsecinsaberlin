#!/usr/bin/env python

from threading import *
import os

global BUFFER_SIZE
BUFFER_SIZE = 1024 # standard buffer size

global stop_all
stop_all = Event()
stop_all.clear()

# *********************************************************
# IP addresses configuration
# *********************************************************
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


# *********************************************************
# Connection with black car
# *********************************************************
global Connection_ON
Connection_ON = Event()
Connection_ON.clear()
global conn_tow
conn_tow = -1
global ConnectionErrorEvent
ConnectionErrorEvent = Event()
ConnectionErrorEvent.clear()