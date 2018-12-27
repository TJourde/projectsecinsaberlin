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
            msg = self.bus.recv()
            
            # Check si l'utilisateur demande la manoeuvre d'approche/accroche du 2e véhicule
            if VB.Approach.isSet():
                
                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------

                # Données US
                if msg.arbitration_id == US1:
                    measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
                    if measured_distance <= HOOKING_DIST:
                        cpt_us_touch += 1
                        if cpt_us_touch == nb_us_touch:
                            US_POS = 'touch'
                    elif measured_distance <=  HOOKING_DIST + 15 and  measured_distance >  HOOKING_DIST :
                        cpt_us_touch = 0
                        cpt_us_close += 1
                        if cpt_us_close == nb_us_close:
                            US_POS = 'close'
                    else: 
                        cpt_us_close = 0
                        cpt_us_touch = 0
                        US_POS = 'away'

                # Données capteur magnétique
                if msg.arbitration_id == HALL:
                    magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                    if magnet_detected:
                        cpt_magnet += 1
                    else: 
                        cpt_magnet
                        FLAG_MAGNET = False
                    if cpt_magnet == nb_magnet_detection:
                        FLAG_MAGNET = True

                # --------------------------------------
                # PART 2 - Traitement des flag et envoi des ordres aux moteurs/solenoid
                # --------------------------------------
                if US_POS == 'touch' and FLAG_MAGNET:
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)
                    time.sleep(1)
                    msg = can.Message(arbitration_id=FROM_PI,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)
                    VB.ApproachComplete.set()
                elif US_POS == 'touch' and not(FLAG_MAGNET):
                    print('Alignment error')
                elif US_POS != 'touch' and FLAG_MAGNET:
                    print('Distance detection error')
                elif US_POS == 'close'
                    print('Slowing down and opening solenoid')
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                    bus.send(msg)
                elif US_POS == 'away'
                    print('Car away, backing in progress')
                    msg = can.Message(arbitration_id=FROM_PI,data=[BACKING_FAST,BACKING_FAST,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)

