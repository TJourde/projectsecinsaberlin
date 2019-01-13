# coding: utf-8

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

    # Bring up CAN0
    print('Bring up CAN0....')
    os.system("sudo ifconfig can0 down")
    time.sleep(0.1)
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)

    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
        print('Connected to bus can')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()
    try:
        sIHM = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sIHM.bind((HOST, PORT))
        sIHM.listen(1)
        conn_IHM, addr = sIHM.accept()
        print('Connected with ' + repr(addr))

        # starting HMI Communications Threads
        newreceive = MyReceive(conn_IHM, bus)
        newreceive.start()
        newsend = MySend(conn_IHM, bus)
        newsend.start()

        # starting communication with pink car
        newtowcom = MyComTow()
        newtowcom.start()

        # launching approach thread (starting procedure only if VB.Approach == True)
        newapproach = Approach(bus)
        newapproach.start()

        # launching error detection thread (starting procedure only if VB.TowingActive == True)
        newdetect = ErrorDetection(bus)
        newdetect.start()

    except KeyboardInterrupt: # Ctrl+C : Stop correctly all the threads
        print('Shutting down all process...')
        VB.stop_all.set()
    except socket.error:
        print('Socket error with connection to IHM')
        print(socket.error)


    newreceive.join()
    newsend.join()
    newtowcom.join()
    newapproach.join()
    newdetect.join()

    s.close()

    print("All process are shut down")
    
