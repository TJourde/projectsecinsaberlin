# coding: utf-8

from threading import *
import time
import can
import os
import struct

#importing Communications Threads
from AvanceManuelle import *

#importing variables linked
import VarBerlin as VB

#importing LidarRegul.py for our regulation
from Remorquage import *

HOST = ''                # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port

# Echo server program
import socket

if __name__ == "__main__":

    #Looking for IP address to "know" which network is used
    ip = os.popen('hostname -I').read() #get chain with '[@IP] \n'
    ip = ip[:len(ip)-2] #(suppress ' \n')

    # Only correct with the two cars black and pink
    if ip == '10.105.1.17': #IOT network
        VB.IpTowing = '10.105.0.55'
    elif ip == '192.168.137.149': #Berlin network
        VB.IpTowing = '192.168.137.31'
    
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        VB.conn, VB.addr = s.accept()
        print('Connected with', VB.addr)

        #starting HMI Communications Threads
        newreceive = MyReceive(VB.conn, bus)
        newreceive.start()
        newsend = MySend(VB.conn, bus)
        newsend.start()

    newreceive.join()
    newsend.join()

    except KeyboardInterrupt:#To finish : Stop correctly all the threads
        VN.stop_all.set()
