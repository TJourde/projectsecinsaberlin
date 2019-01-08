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

global IpBlack
global IpPink

HOST = ''                # Symbolic name meaning all available interfaces
PORT = 6666              # Arbitrary non-privileged port


if __name__ == "__main__":

    # Looking for IP address to "know" which network is used
    IpBlack = os.popen('hostname -I').read() # get chain with '[@IP] \n'
    IpBlack = IpBlack[:len(IpBlack)-2] # (suppress ' \n')

    # Only correct with the two cars black and pink
    if IpBlack == '10.105.0.55': # IOT network
        VB.IpRose = '10.105.0.53'
    elif IpBlack == '192.168.137.201': # Berlin network
        VB.IpRose = '192.168.137.12'

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

        # starting HMI Communications Threads
        newreceive = MyReceive(VB.conn, bus)
        newreceive.start()
        newsend = MySend(VB.conn, bus)
        newsend.start()

        # starting communication with pink car
        newtowcom = MyTowCom(VB.IpTowing)
        newtowcom.start

        # launching approach thread (starting procedure only if VB.Approach == True)
        newapproach = Approach(bus)
        newapproach.start

        # launching error detection thread (starting procedure only if VB.TowingActive == True)
        newdetect = ErrorDetection(bus)
        newdetect.start

    except KeyboardInterrupt: # Ctrl+C : Stop correctly all the threads
        VB.stop_all.set()
        print('Shutting down all process...')
    except socket.error:
        print('Socket error')

    newreceive.join()
    newsend.join()
    newtowcom.join()
    newapproach.join()
    newdetect.join()

    VB.conn.close()

    print("All process are shut down")
    