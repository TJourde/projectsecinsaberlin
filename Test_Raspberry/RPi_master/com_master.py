# coding: utf-8

from threading import *
import time
import can
import os
import struct
import socket

#importing variables linked
import VarBerlin as VB

'''
#importing Communications Threads
from Platooning_thread import *
'''

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102
HALL = 0x103

'''
 Messages envoyés :
    - ultrason avant gauche
    header : UFL payload : entier, distance en cm
    - ultrason avant centre
    header : UFC payload : entier, distance en cm
    - ultrason avant droite
    header : UFR payload : entier, distance en cm
    - ultrason arriere gauche
    header : URL payload : entier, distance en cm
    - ultrason arriere centre
    header : URC payload : entier, distance en cm
    - ultrason arriere droite
    header : URR payload : entier, distance en cm
    - position volant
    header : POS payload : entier, valeur brute du capteur
    - vitesse roue gauche
    header : SWL payload : entier, *0.01rpm
    - vitesse roue droite
    header : SWR payload : entier, *0.01rpm
    - Niveau de la batterie
    header : BAT payload : entier, mV
    - Pitch
    header : PIT payload : float, angle en degrée
    - Yaw
    header : YAW payload : float, angle en degrée
    - Roll
    header : ROL payload : float, angle en degrée

 Messages reçus :
    - Modification de la vitesse
    header : SPE payload : valeur entre 0 et 50
    - Control du volant (droite, gauche)
    header : STE paylaod : left | right | stop
    - Control de l'avancée
    header : MOV payload : forward | backward | stop
    - Controle de la position du Solenoid
    header : SOL payload : up | down
    - Controle du mode "towing"
    header : TOW payload : request | on | resume | off
'''

# *********************************************************
# THREAD 1 - Récupération des données du CAN ou interne à la RPi, envoi à l'application
# *********************************************************

class MySend(Thread):

    def __init__(self, conn, bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus = bus
        print(self.getName(), 'initialized')

    def run(self):
        while True :
            
            msg = self.bus.recv()
            
            if msg.arbitration_id == US1:
                # ultrason avant gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "UFL:" + str(distance) + ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason avant droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "UFR:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason arriere centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "URC:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "URL:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "URR:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "UFC:" + str(distance)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == MS:
                # position volant
                angle = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "POS:" + str(angle)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # Niveau de la batterie
                bat = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "BAT:" + str(bat)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # vitesse roue gauche
                speed_left = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "SWL:" + str(speed_left)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # vitesse roue droite
                speed_right= int.from_bytes(msg.data[6:8], byteorder='big')
                message = "SWR:" + str(speed_right)+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == OM1:
                # Yaw
                yaw = struct.unpack('>f',msg.data[0:4])
                message = "YAW:" + str(yaw[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
                # Pitch
                pitch = struct.unpack('>f',msg.data[4:8])
                message = "PIT:" + str(pitch[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == OM2:
                # Roll
                roll = struct.unpack('>f',msg.data[0:4])
                message = "ROL:" + str(roll[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif msg.arbitration_id == HALL:
                # capteur magnétique
                magnetic_sensor = struct.unpack('>f',msg.data[0:1])
                message = "MAG:" + str(magnetic_sensor[0])+ ";"
                size = self.conn.send(message.encode())
                if size == 0: break


            # Valeurs propres au towing
            if VB.ApproachComplete.is_set():
                VB.ApproachComplete.clear()
                message = "TOWSTATE:ApproachComplete;"
                size = self.conn.send(message.encode())
                if size == 0: break
            if VB.CodeSem.acquire():
                message = "ERR:" + VB.CodeErreur
                size = self.conn.send(message.encode())
                VB.ProbSem.release()
                if size == 0: break




# *********************************************************
# THREAD 2 - Réception des données de l'application, envoi des commandes sur le CAN + modification variables internes
# *********************************************************

class MyReceive(Thread):
    def __init__(self,conn, bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.speed_cmd = 0
        self.position_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        self.position = 0
        print(self.getName(), 'initialized')

    def run(self):
        self.speed_cmd = 0
        self.position_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        self.position = 0   
        
        while True :
            data = self.conn.recv(1024)
            data = str(data)
            data = data[2:len(data)-1]

            if not data: break
            
            #split each command received if there are more of 1 
            for cmd in data.split(';'):
                print('val cmd : ',cmd)
                
                # don't try an empty command
                if not cmd: continue 
                
                #split the dealed command in header and payload (command = 'header:payload;')
                header, payload = cmd.split(':')
                print("header :", header, " payload:", payload)
                
                #Deal with the command
                if (header == 'SPE'):  # speed
                    self.speed_cmd = int(payload)
                    print("speed is updated to ", self.speed_cmd)
                elif (header == 'POS'): # front wheels position
                    self.position_cmd = int(payload)
                    print("steering wheels position is updated to ", self.position_cmd)
                    self.pos = 1
                    self.enable = 1
                elif (header == 'STE'):  # steering
                    if (payload == 'left'):
                        self.turn = -1
                        self.enable = 1
                        print("Turn left")
                    elif (payload == 'right'):
                        self.turn = 1
                        self.enable = 1
                        print("Turn right")
                    elif (payload == 'stop'):
                        self.turn = 0
                        self.enable = 1
                        print("Stop turn")
                elif (header == 'MOV'):  # move
                    if (payload == 'stop'):
                        self.move = 0
                        self.enable = 1
                        print("Stop")
                    elif (payload == 'forward'):
                        print("Move forward")
                        self.move = 1
                        self.enable = 1
                    elif (payload == 'backward'):
                        print("Move backward")
                        self.move = -1
                        self.enable = 1
                elif (header == 'TOW'):
                    if (payload == 'request'):
                        print("Starting connection & approach")
                        VB.Connect.set() # initiate connection
                        VB.Approach.set() # start approaching the 2nd car
                        self.enable = 0
                    if (payload == 'on'):
                        print("Starting towing mode")
                        VB.Approach.clear() # stop approaching the 2nd car
                        VB.TowingActive.set() # start error detection
                        self.enable = 1
                    if (payload == 'resume'):
                        print("Resume towing")
                        VB.TowingActive.set()
                    if (payload == 'off'):
                        print("Stopping towing mode")
                        VB.Connect.clear() # closing communication with 2nd car
                        VB.TowingActive.clear() # stop error detection

                # In case of an error detection while towing
                if VB.ProbSem.acquire() and VB.TowingActive.is_set() and VB.SourceProb != -1:
                    enable = 0

                print(self.speed_cmd)
                print(self.move)
                print(self.turn)
                print(self.enable)

                #edition des commandes de mouvement si enabled
                if self.enable:

                    #Speed Command
                    if self.move == 0:
                        cmd_mv = (50 + self.move*self.speed_cmd) & ~0x80
                    else:
                        cmd_mv = (50 + self.move*self.speed_cmd) | 0x80

                    #Steering Command
                    if self.turn == 0:
                        cmd_turn = 50
                        #cmd_turn = 50 +self.turn*20 & 0x80
                    else:
                        if self.turn == 1:
                            cmd_turn = 100
                        else:
                            cmd_turn = 0
                        cmd_turn |= 0x80
                        #cmd_turn = 50 + self.turn*20 | 0x80
                        
                    #Steering position command
                    if self.pos == 0:
                        cmd_pos = self.position_cmd & ~0x80
                    else:
                        cmd_pos = self.position_cmd | 0x80

                    #Recap
                    print("mv:",cmd_mv,"turn:",cmd_turn,"pos:",cmd_pos)
                    #Create message
                    msg = can.Message(arbitration_id=MCM,data=[cmd_mv, cmd_mv, cmd_turn, cmd_pos, 0, 0, 0, 0], extended_id=False)
                    print(msg)
                    #Send message
                    self.bus.send(msg)

        self.conn.close()
        