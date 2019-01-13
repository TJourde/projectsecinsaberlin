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
    header : STE payload : left | right | stop
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
        print(self.getName(), '****** MySend initialized')

    def run(self):
        while True :

            if VB.stop_all.is_set():break
            
            try:
                msg = self.bus.recv(0.2)
            
                # --------------------------------------
                # PART 1 - Native messages
                # --------------------------------------
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
                
                # --------------------------------------
                # PART 2 - Towing-related messages
                # --------------------------------------
                # capteur magnétique
                elif msg.arbitration_id == HALL:
                    magnetic_sensor = int.from_bytes(msg.data[0:1], byteorder='big')
                    message = "MAG:" + str(magnetic_sensor)+ ";"
                    size = self.conn.send(message.encode())
                    if size == 0: break
            except: pass
        
            # connexion voiture rose
            if VB.Connection_ON.is_set():
                message = "CON_PINK:on;"
                size = self.conn.send(message.encode())
                if size == 0: break
            else:
                message = "CON_PINK:off;"
                size = self.conn.send(message.encode())
                if size == 0: break

            # etat voiture noire
            if VB.Approach.is_set():
                message = "STATE:approaching;"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif VB.Hooking_ON.is_set():
                message = "STATE:approach_complete;"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif VB.Towing_ON.is_set():
                message = "STATE:towing;"
                size = self.conn.send(message.encode())
                if size == 0: break
            elif VB.Towing_Error.is_set():
                message = "STATE:towing_error;"
                size = self.conn.send(message.encode())
                if size == 0: break             
            else:
                message = "STATE:idle;"
                size = self.conn.send(message.encode())
                if size == 0: break

            # code d'erreur pendant remorquage
            if VB.Towing_Error.is_set():
                if VB.ErrorCodeSem.acquire(False):
                    message = "ERR:" + str(VB.ErrorCode) + ";"
                    VB.ErrorCodeSem.release()
                    size = self.conn.send(message.encode())
                    if size == 0: break

            
'''
            # Valeurs propres au towing
            if not(VB.ConnectComplete.is_set() and VB.ApproachComplete.is_set() and VB.TowingActive.is_set()):
                message = "STATE:Idle"
                size = self.conn.send(message.encode())
                if size == 0: break
            if VB.ConnectComplete.is_set():
                message = "STATE:ConnectComplete"
                size = self.conn.send(message.encode())
                if size == 0: break
            if VB.ApproachComplete.is_set():
                message = "STATE:Hooking;"
                size = self.conn.send(message.encode())
                if size == 0: break
            if VB.TowingError.is_set():
                if VB.CodeSem.acquire(false):
                    message = "ERR:" + VB.CodeErreur
                    size = self.conn.send(message.encode())
                    VB.CodeSem.release()
                if size == 0: break
'''



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
        self.pos = 0
        print(self.getName(), '****** MyReceive initialized')

    def run(self):
        self.speed_cmd = 0
        self.position_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        self.pos = 0   

        while True :

            if VB.stop_all.is_set():break

            #self.conn.setblocking(0)
            #try:
            data = self.conn.recv(50)
            data = str(data)
            data = data[2:len(data)-1]

            if not data: break

            print(self.getName(),data)
            #except IOError as e:
             #   pass
            
            
            #split each command received if there are more of 1 
            for cmd in data.split(';'):
                #print(self.getName(),'val cmd : ',cmd)
                
                # don't try an empty command
                if not cmd: continue 
                
                #split the dealed command in header and payload (command = 'header:payload;')
                header, payload = cmd.split(':')
                print("header :", header, " payload:", payload)
                
                # --------------------------------------
                # PART 1 - Native messages
                # --------------------------------------                
                # speed
                if (header == 'SPE'): 
                    self.speed_cmd = int(payload)
                    print("speed is updated to ", self.speed_cmd)
                # steering
                elif (header == 'STE'):  
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
                # move
                elif (header == 'MOV'):  
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


                # --------------------------------------
                # PART 2 - Towing-related messages
                # --------------------------------------
                # front wheels position
                elif (header == 'POS'): 
                    self.position_cmd = int(payload)
                    print(self.getName(),"steering wheels position is updated to ", self.position_cmd)
                    self.pos = 1
                    self.enable = 1
                # hooking related commands
                elif (header == 'HOO'):
                    if (payload == 'start'):
                        print(self.getName(),'Start hooking manoeuver')
                        self.enable = 0
                        VB.Connect.set()
                        VB.Approach.set()
                        self.enable = 0
                    if (payload == 'stop'):
                        print(self.getName(),'Stopping hooking manoeuver')
                        VB.Connect.clear()
                        VB.Connection_ON.clear()
                        VB.Approach.clear()
                        VB.Disconnect.set()
                # towing related commands
                elif (header == 'TOW'):
                    if (payload == 'start'):
                        print(self.getName(),'Starting towing mode - error detection ON')
                        VB.Towing_ON.set()
                    if (payload == 'stop'):
                        print(self.getName(),'Stopping towing mode - error detection OFF - disconnected from pink car')
                        VB.Towing_ON.clear()
                        VB.Towing_OFF.set()
                        VB.Connection_ON.clear()
                        VB.Disconnect.set()

                #print(self.speed_cmd)
                #print(self.move)
                #print(self.turn)
                #print(self.enable)

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

#        self.conn.close()
        
