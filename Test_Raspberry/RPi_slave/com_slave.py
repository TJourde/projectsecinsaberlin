#!/usr/bin/env python

# coding: utf-8
from threading import Thread
import time
import can
import os
import struct

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102


'''
 Messages envoyés :
    - ultrason avant gauche
    header : UFL_slave payload: entier, distance en cm
    - ultrason avant centre
    header : UFC_slave payload: entier, distance en cm
    - ultrason avant droite
    header : UFR_slave payload: entier, distance en cm
    - ultrason arriere gauche
    header : URL_slave payload: entier, distance en cm
    - ultrason arriere centre
    header : URC_slave payload: entier, distance en cm
    - ultrason arriere droite
    header : URR_slave payload: entier, distance en cm
    - position volant
    header : POS_slave payload: entier, valeur brute du capteur
    - vitesse roue gauche
    header : SWL_slave payload: entier, *0.01rpm
    - vitesse roue droite
    header : SWR_slave payload: entier, *0.01rpm
    - Niveau de la batterie
    header : BAT_slave payload: entier, mV
    - Pitch
    header : PIT_slave payload: float, angle en degrée
    - Yaw
    header : YAW_slave payload: float, angle en degrée
    - Roll
    header : ROL_slave payload: float, angle en degrée

 Messages reçus :
    - Modification de la vitesse
    header : SPE_slave payload: valeur entre 0 et 50
    - Control du volant (droite, gauche)
    header : STE_slave paylaod: left | right | stop
    - Contra l de l'avancée
    header : MOV_slave payload: forward | backward | stop
'''





class MySendSlave(Thread):

    def __init__(self,socket, bus):
        Thread.__init__(self)
        self.socket = socket
        self.bus = bus
        print(self.getName(), 'MySend initialized')

    def run(self):
        while True :
            msg = self.bus.recv()

            if msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "URL_slave:" + str(distance)+ ";"
                #size = self.socket.send(message.encode())
                #if size == 0: break
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "URR_slave:" + str(distance)+ ";"
                #size = self.socket.send(message.encode())
                #if size == 0: break
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "UFC_slave:" + str(distance)+ ";"
                size = self.socket.send(message.encode())
                if size == 0: break

class MyReceiveSlave(Thread):
    def __init__(self,socket, bus):
        Thread.__init__(self)
        self.socket = socket
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
            self.speed_cmd = 0
        socket.close()