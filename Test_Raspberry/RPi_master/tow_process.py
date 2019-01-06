# coding: utf-8
from threading import Thread
import queue
import time
import can
import os
import struct
import socket

# importing local threads
import VarBerlin as VB


# ******************************
# Variables locales
# ******************************

# IDENTIFIANT MESSAGE
US1 = 0x000
US2 = 0x001
MCM = 0x010 #cmde moteur
MS = 0x100
OM1 = 0x101
OM2 = 0x102
HALL= 0x103

# COMMANDES SOLENOID
SOLENOID_UP = 0xFF
SOLENOID_DOWN = 0x00

# COMMANDES ROUES
NO_MOVE = 0xB1
BACKING_FAST = 0xA0
BACKING_SLOW = 0xAD
WHEELS_CENTER = 0xB1
cmd_mv = 0
cmd_pos = 0

# Données distance US/état capteur magnet
measured_distance = -1
magnet_detected = -1
HOOKING_DIST = 30
LIMIT_DIST = 35
# Compteur et auxiliaire
cpt_us_close = 0
cpt_us_touch = 0
cpt_magnet = 0
nb_us_close = 3
nb_us_touch = 3
nb_magnet_detection = 3
# Flag US/Magnet
US_POS = 'away' # valeur: away | close | touch
FLAG_MAGNET = False


# ******************************
# THREAD 1 - Procédure d'approche
# ******************************
class Approach(Thread)
    
    def __init__(self, bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')

        # Compteurs et valeurs limites
        self.cpt_us_close = 0
        self.cpt_us_touch = 0
        self.cpt_magnet = 0
        self.nb_us_close = 3
        self.nb_us_touch = 3
        self.nb_magnet_detection = 3
        # Flag US/Magnet
        self.US_POS = 'away' # valeur: away | close | touch
        self.FLAG_MAGNET = False

        print(self.getName(), 'initialized')

    def run(self):

        self.cpt_us_close = 0
        self.cpt_us_touch = 0
        self.cpt_magnet = 0
        self.nb_us_close = 3
        self.nb_us_touch = 3
        self.nb_magnet_detection = 3
        self.US_POS = 'away'
        self.FLAG_MAGNET = False

        while True:
            msg = self.bus.recv()
            
            # Check si l'utilisateur demande la manoeuvre d'approche/accroche du 2e véhicule
            if VB.Approach.is_set():
                
                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------

                # Données US
                if msg.arbitration_id == US1:
                    measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
                    if measured_distance <= HOOKING_DIST:
                        self.cpt_us_touch += 1
                        # self.cpt_us_close = 0 ----> Non placé car permet de reculer et d'arriver en dessous de la HOOKING_DIST
                        if self.cpt_us_touch == self.nb_us_touch:
                            self.cpt_us_close = 0
                            self.US_POS = 'touch'
                    elif measured_distance > HOOKING_DIST and measured_distance <= HOOKING_DIST + 15:
                        self.cpt_us_touch = 0
                        self.cpt_us_close += 1
                        if self.cpt_us_close == self.nb_us_close:
                            self.US_POS = 'close'
                    else: 
                        self.cpt_us_close = 0
                        self.cpt_us_touch = 0
                        self.US_POS = 'away'

                # Données capteur magnétique
                if msg.arbitration_id == HALL:
                    magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                    if magnet_detected:
                        self.cpt_magnet += 1
                    else:
                        self.FLAG_MAGNET = False
                    if self.cpt_magnet == self.nb_magnet_detection:
                        self.FLAG_MAGNET = True

                # --------------------------------------
                # PART 2 - Traitement des flag et envoi des commandes aux moteurs/solenoid
                # --------------------------------------
                if self.US_POS == 'touch' and self.FLAG_MAGNET:
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)
                    time.sleep(1)
                    msg = can.Message(arbitration_id=FROM_PI,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)
                    VB.ApproachComplete.set()
                elif self.US_POS == 'touch' and not(self.FLAG_MAGNET):
                    print('Alignment error')
                elif self.US_POS != 'touch' and self.FLAG_MAGNET:
                    print('Distance detection error')
                elif self.US_POS == 'close'
                    print('Slowing down and opening solenoid')
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                    bus.send(msg)
                elif self.US_POS == 'away'
                    print('Car away, backing in progress')
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_FAST,BACKING_FAST,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)



# ******************************
# THREAD 2 - Détection d'erreur pendant le remorquage
# ******************************
class ErrorDetection(Thread)

    def __init__(self, bus):
        Thread.__init__(self)
        self.bus = bus

        # Valeurs données
        self.distance_us = -1
        self.distance_us3 = -1
        self.magnet_detected = -1
        # Compteurs
        self.cpt_us = 0
        self.cpt_us3 = 0
        self.cpt_cm = 0
        self.cpt_multi = 0
        # Valeurs limites
        self.limit_us = 3
        self.limit_us3 = 3
        self.limit_cm = 3
        self.limit_multi = 3
        # Flag US/Magnet
        self.trame = False
        self.FLAG_US = False
        self.FLAG_US3 = False
        self.FLAG_CM = False

        print(self.getName(), 'initialized')

    def run(self):
        while True:
            msg = self.bus.recv()
            
            # Check si l'utilisateur demande l'activation du remorquage (donc du mode détection d'erreurs)
            if VB.TowingActive.is_set():

                # Check si la 2e voiture est bien connectée, sinon arrête le remorquage
                if VB.US3 == -1:
                    print('No connection with 2nd car, ', self.getName(), ' is suspended' )

                else

                    # --------------------------------------
                    # PART 1 - Traitement des données et levée des flag
                    # --------------------------------------

                    # Données US
                    if msg.arbitration_id == US1:
                        distance_us = int.from_bytes(msg.data[4:6], byteorder='big')
                        if distance_us > LIMIT_DIST:
                            cpt_us += 1
                        else: cpt_us = 0
                        if cpt_us == limit_us:
                            FLAG_US = True

                    # Données US3
                    self.distance_us3 = VB.US3
                    if distance_us3 > LIMIT_DIST:
                        cpt_us3 += 1
                    else: cpt_us3 = 0
                    if cpt_us3 == limit_us3:
                        FLAG_US3 = True

                    # Données CM
                    if msg.arbitration_id == HALL:
                        magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                        if magnet_detected == 0:
                            cpt_cm += 1
                        else: cpt_cm = 0
                        if cpt_cm == limit_cm:
                            FLAG_CM = True

                    # --------------------------------------
                    # PART 2 - Traitement des flag
                    # --------------------------------------
                    if FLAG_CM or FLAG_US or FLAG_US3:
                        msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
                        self.bus.send(msg)
                        cpt_multi += 1

                    if cpt_multi == limit_multi:
                        if FLAG_CM and FLAG_US and FLAG_US3:


