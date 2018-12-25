# coding: utf-8

from threading import *
import socket
import queue

#importing variables linked
import VarBerlin as VB


MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102
HALL = 0x103

TCP_IP = '10.105.0.55'
TCP_PORT = 9052
BUFFER_SIZE = 8  # Normally 1024, but we want fast response

# Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
class MyTransmitTow(Thread)
    
    def __init__(self,bus):
        Thread.__init__(self)
        self.bus = bus
        print(self.getName(), 'initialized')

    def run(self):
        while True :
            print("Attempt to connect to second car\n")

