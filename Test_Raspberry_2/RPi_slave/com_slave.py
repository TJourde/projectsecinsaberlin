#!/usr/bin/env python

# coding: utf-8
from threading import Thread
import time
import can
import os
import struct
import socket

import VarBerlin_slave as VBS

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

TCP_PORT = 9000
BUFFER_SIZE = 20


# *********************************************************
# THREAD 1 - Connection à la voiture noire
# *********************************************************
class MyComSlave(Thread):
    def __init__(self,IpPink,IpBlack):
        Thread.__init__(self)
        self.addr = -1
        self.IpPink = VBS.IpPink
        self.IpBlack = VBS.IpBlack
        print(self.getName(), 'MyComSlave initialized')

    def run(self):
        while True:

            # Check si aucune connection n'est en cours
            if self.addr == -1:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.bind((self.IpPink,TCP_PORT))
                    s.listen()
                    print('Pink car ready to receive connection')
                    VBS.conn, self.addr = s.accept()
                except socket.error:
                    VBS.conn.close()
                    print('Socket error while receiving connection')

            # Check si l'adresse connectée est bien celle de la voiture noire, si oui commence l'envoi des données
            elif (self.addr == self.IpBlack):
                print('Connected to Berlin car with address' + repr(self.addr))
                Connection_ON.set()

            # Si quelqu'un autre que la RPi noire se connecte, le déclare, clôt la connection et se met en attente d'une nouvelle
            elif (self.addr != self.IpBlack):
                Connection_ON.clear()
                print('Connected to unknown device, with address ' + repr(self.addr))
                print('Closing communication channel')
                VBS.conn.close()
                self.addr = -1



# *********************************************************
# THREAD 2 - Envoi de message à la voiture noire
# *********************************************************
class MySendSlave(Thread):

    def __init__(self,bus):
        Thread.__init__(self)
        self.bus = bus
        print(self.getName(), 'MySend initialized')

    def run(self):
        while True :
            msg = self.bus.recv()
            if not VBS.Connection_ON.is_set():
                conn = VBS.conn
                if msg.arbitration_id == US2:
                    # ultrason avant centre
                    distance_us3 = int.from_bytes(msg.data[4:6], byteorder='big')
                    message = "UFC_slave:" + str(distance_us3)+ ";"
                    size = conn.send(message.encode())
                    if size == 0: break



# *********************************************************
# THREAD 3 - Réception de messages depuis la voiture noire
# *********************************************************
class MyReceiveSlave(Thread):
    def __init__(self,bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        print(self.getName(), 'MyReceive initialized')

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True :
            pass