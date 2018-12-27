# coding: utf-8

'''
# -- change the ip addresses of the BERLIN NETWORK
'''

from threading import *
import time
import can
import os
import socket
import struct

#importing normal communication threads
from com_master import *

#importing towing communication threads
from com_tow import *  

#importing error detection during towing
from tow_process import *

#importing variables linked
import VarBerlin as VB


HOST = ''                # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port


if __name__ == "__main__":

    #Looking for IP address to "know" which network is used
    ip = os.popen('hostname -I').read() #get chain with '[@IP] \n'
    ip = ip[:len(ip)-2] #(suppress ' \n')

    # Only correct with the two cars black and pink
    if ip == '10.105.1.17': #IOT network
        VB.IpTowing = '10.105.0.55'
        VB.IpRose = '10.105.0.53'
    elif ip == '192.168.137.149': #Berlin network
        VB.IpTowing = '192.168.137.'
        VB.IpRose = '192.168.137.'
    
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
        print('Connected with ' + repr(VB.addr))

        #starting HMI Communications Threads
        newreceive = MyReceive(VB.conn, bus)
        newreceive.start()
        newsend = MySend(VB.conn, bus)
        newsend.start()

        #starting communication with pink car
        newtowcom = MyTowCom(VB.conn,IpTowing)
        newtowcom.start

    except KeyboardInterrupt:#To finish : Stop correctly all the threads
        VB.stop_all.set()
    	print("Shutting down all processes...")

    newreceive.join()
    newsend.join()
    newtowcom.join()

    print("All processes are shut down")
    