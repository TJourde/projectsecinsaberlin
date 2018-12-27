# coding: utf-8
from threading import Thread
import queue
import time
import can
import os
import struct
import socket

US1 = 0x000
US2 = 0x001
MCM = 0x010 #cmde moteur
MS = 0x100
OM1 = 0x101
OM2 = 0x102
HALL= 0x103

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

class Approach(Thread)
    
     def __init__(self, bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        print(self.getName(), 'initialized')

    def run(self):
        while True:
            if VB.Approach.isSet():
                
