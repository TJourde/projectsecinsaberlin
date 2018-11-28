# coding: utf-8
from threading import Thread
import time
import can
import os
import struct

MCM = 0x010 #cmde moteur
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102
Hall= 0x103
'''

    - ULTRASON AVANT GAUCHE
    HEADER : UFL PAYLOAD : ENTIER, DISTANCE EN CM
    - ULTRASON AVANT CENTRE
    HEADER : UFC PAYLOAD : ENTIER, DISTANCE EN CM
    - ULTRASON AVANT DROITE
    HEADER : UFR PAYLOAD : ENTIER, DISTANCE EN CM
    - ULTRASON ARRIERE GAUCHE
    HEADER : URL PAYLOAD : ENTIER, DISTANCE EN CM
    - ULTRASON ARRIERE CENTRE
    HEADER : URC PAYLOAD : ENTIER, DISTANCE EN CM
    - ULTRASON ARRIERE DROITE
    HEADER : URR PAYLOAD : ENTIER, DISTANCE EN CM
    - POSITION VOLANT
    HEADER : POS PAYLOAD : ENTIER, VALEUR BRUTE DU CAPTEUR
    - VITESSE ROUE GAUCHE
    HEADER : SWL PAYLOAD : ENTIER, *0.01RPM
    - VITESSE ROUE DROITE
    HEADER : SWR PAYLOAD : ENTIER, *0.01RPM
    - NIVEAU DE LA BATTERIE
    HEADER : BAT PAYLOAD : ENTIER, MV
    - PITCH
    HEADER : PIT PAYLOAD : FLOAT, ANGLE EN DEGRÉE
    - YAW
    HEADER : YAW PAYLOAD : FLOAT, ANGLE EN DEGRÉE
    - ROLL
    HEADER : ROL PAYLOAD : FLOAT, ANGLE EN DEGRÉE

    - MODIFICATION DE LA VITESSE
    HEADER : SPE PAYLOAD : VALEUR ENTRE 0 ET 50
    - Control du volant (droite, gauche)
    header : STE paylaod : left | right | stop
    - Contra l de l'avancée
    header : MOV payload : forward | backward | stop
'''

print ('Envoi test\n')


try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

while True :
    msg = bus.recv()
    Magnet=0
    if msg.arbitration_id == US1:
# ultrason avant gauche
        distance = int.from_bytes(msg.data[0:2], byteorder='big')
        message = "UFL:" + str(distance) + ";"
#        print(message)
# ultrason avant droit
        distance = int.from_bytes(msg.data[2:4], byteorder='big')
        message = "UFR:" + str(distance)+ ";"
#        print(message)
# ultrason arriere centre
        distance = int.from_bytes(msg.data[4:6], byteorder='big')
        message = "URC:" + str(distance)+ ";"
        print(message)
    elif msg.arbitration_id == US2:
# ultrason arriere gauche
        distance = int.from_bytes(msg.data[0:2], byteorder='big')
        message = "URL:" + str(distance)+ ";"
#        print(message)
# ultrason arriere droit
        distance = int.from_bytes(msg.data[2:4], byteorder='big')
        message = "URR:" + str(distance)+ ";"
#        print(message)
# ultrason avant centre
        distance = int.from_bytes(msg.data[4:6], byteorder='big')
        message = "UFC:" + str(distance)+ ";"
#        print(message)
    elif msg.arbitration_id == OM1:
 # Yaw
        yaw = struct.unpack('>f',msg.data[0:4])
        message = "YAW:" + str(yaw[0])+ ";"
#        print (message)
    elif msg.arbitration_id == Hall:
        Magnet=int.from_bytes(msg.data[0:1],byteorder='big')
        print(Magnet)
        if Magnet==1:
           print("loin")
        elif Magnet==0:
           print("atache")

#valeurs à envoyer = %
#max = FF(255)
#50% de FF = 80(128)
#60%(98)
#40%(66)

#25%(3F)
#75%(BF)

#define MAX_SPEED_STEERING 60
#define MIN_SPEED_STEERING 40

#define MAX_SPEED_WHEEL 75
#define MIN_SPEED_WHEEL 25

#données pour signal pendant 1 s
#BC marche avant
#CA marche avant max
#0x80 marche arrière max
#1: Roue arriere gauche
#2: Roue arrière droite

#BC vers la gauche
#0x80 vers la droite max
#0xB8 pour milieu si à droite max
#3: Roues avant gauche

#Reste est inutile pour 0x010
'''
time.sleep(1)
msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
bus.send(msg)
'''




