#!/usr/bin/env python

from threading import *
import os

global BUFFER_SIZE
BUFFER_SIZE = 1024 # standard buffer size


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

if '10.105.0.53' in IpPink: #IOT Network
	IpPink = '10.105.0.53'
	IpBlack = '10.105.0.55'
if '192.168.137.135' in IpPink:  # Berlin network
	IpPink = '192.168.137.135'
	IpBlack = '192.168.137.27'
elif '192.168.1.21' in IpPink: # Grenier network
	IpPink = '192.168.1.21'
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