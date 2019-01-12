#!/usr/bin/env python

from threading import *
import os

global Connection_ON
Connection_ON = Event()
global conn
conn = -1

global IpBlack
global IpPink

# Search own IP address to know which network it's on
IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
if IpPink == '10.105.0.53': # IOT network
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    IpBlack = '192.168.137.27'
elif IpPink == '192.168.1.21': # Grenier network
    IpBlack = '192.168.1.20'