#!/usr/bin/env python

from threading import *
import os

global Connection_ON
Connection_ON = Event()
global conn
conn = -1


# Search own IP address to know which network it's on
IpPink = os.popen('hostname -I').read() #get chain with '[@IP] \n'
global IpPink
IpPink = IpPink[:len(IpPink)-2] #(suppress ' \n')
if IpPink == '10.105.0.53': # IOT network
    global IpBlack
    IpBlack = '10.105.0.55'
elif IpPink == '192.168.137.12': # Berlin network
    global IpBlack
    IpBlack = '192.168.137.27'
elif IpPink == '192.168.1.21': # Grenier network
    global IpBlack
    IpBlack = '192.168.1.20'