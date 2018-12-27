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





class MySend(Thread):

    def __init__(self,conn, bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus = bus

    def run(self):
        while True :
            msg = self.bus.recv()

'''
            if msg.arbitration_id == US1:
                # ultrason avant gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "UFL_slave:" + str(distance) + ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason avant droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "UFR_slave:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason arriere centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "URC_slave:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
'''
            if msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "URL_slave:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "URR_slave:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "UFC_slave:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
'''
            elif msg.arbitration_id == MS:
                # position volant
                angle = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "POS_slave:" + str(angle)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # Niveau de la batterie
                bat = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "BAT_slave:" + str(bat)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # vitesse roue gauche
                speed_left = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "SWL_slave:" + str(speed_left)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # vitesse roue droite
                speed_right= int.from_bytes(msg.data[6:8], byteorder='big')
                message = "SWR_slave:" + str(speed_right)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == OM1:
                # Yaw
                yaw = struct.unpack('>f',msg.data[0:4])
                message = "YAW_slave:" + str(yaw[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # Pitch
                pitch = struct.unpack('>f',msg.data[4:8])
                message = "PIT_slave:" + str(pitch[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == OM2:
                # Roll
                roll = struct.unpack('>f',msg.data[0:4])
                message = "ROL_slave:" + str(roll[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
'''


class MyReceive(Thread):
    def __init__(self,conn, bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')

        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True :
'''
            data = conn.recv(1024)

            if not data: break

            #for b in data:
            #    print(b)

            header = data[0:3]
            payload = data[3:]
            print("header :", header, "payload:", str(payload))

            if (header == b'SPE'):  # speed
                self.speed_cmd = int(payload)
                print("speed is updated to ", self.speed_cmd)
            elif (header == b'STE'):  # steering
                if (payload == b'left'):
                    self.turn = 1
                    self.enable = 1
                    print("send cmd turn left")
                elif (payload == b'right'):
                    self.turn = -1
                    self.enable = 1
                    print("send cmd turn right")
                elif (payload == b'stop'):
                    self.turn = 0
                    self.enable = 0
                    print("send cmd stop to turn")
            elif (header == b'MOV'):  # move
                if (payload == b'stop'):
                    self.move = 0
                    self.enable = 0
                    print("send cmd move stop")
                elif (payload == b'forward'):
                    print("send cmd move forward")
                    self.move = 1
                    self.enable = 1
                elif (payload == b'backward'):
                    print("send cmd move backward")
                    self.move = -1
                    self.enable = 1

            print(self.speed_cmd)
            print(self.move)
            print(self.turn)
            print(self.enable)

            if self.enable:
                cmd_mv = (50 + self.move*self.speed_cmd) | 0x80
                cmd_turn = 50 + self.turn*20 | 0x80
            else:
                cmd_mv = (50 + self.move*self.speed_cmd) & ~0x80
                cmd_turn = 50 + self.turn*20 & 0x80

            print("mv:",cmd_mv,"turn:",cmd_turn)

            msg = can.Message(arbitration_id=MCM,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)

            #msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            #msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            print(msg)
            self.bus.send(msg)
'''
        conn.close()