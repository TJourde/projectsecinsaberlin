#!/usr/bin/env python

import struct
import os
import can
import socket

#importing towing variables
import VarBerlin as VB


#Looking for IP address to "know" which network is used
ip = os.popen('hostname -I').read() #get chain with '[@IP] \n'
ip = ip[:len(ip)-2] #(suppress ' \n')
# Only correct with the two cars black and pink
if ip == '10.105.1.13': # IOT network
    VB.IpTowing = '10.105.0.55'
elif ip == '192.168.137.12': # Berlin network
    VB.IpTowing = '192.168.137.201'


TCP_PORT = 9000
BUFFER_SIZE = 20

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((VB.IpTowing,TCP_PORT))
    print('Connected with towing car with address ', VB.addr)
except socket.error():
	print('Connection error')
except KeyboardInterrupt:#To finish : Stop correctly all the threads
    VN.stop_all.set()


newreceiveslave = MyReceiveSlave(conn, bus)
newreceiveslave.start()
newsendslave = MySendSlave(conn, bus)
newsendslave.start()

newreceiveslave.join()
newsendslave.join()















TCP_IP = '10.1.5.224'
TCP_PORT = 9050
BUFFER_SIZE = 20
MESSAGE = bytes('aBcDeF', encoding='utf_8')


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    VB.conn, VB.addr = s.accept()
    print('Connected with towing car with address ', VB.addr)


except KeyboardInterrupt:#To finish : Stop correctly all the threads
    VN.stop_all.set()

