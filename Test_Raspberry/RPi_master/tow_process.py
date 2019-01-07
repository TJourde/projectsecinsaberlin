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


# ******************************
# THREAD 4 - Procédure d'approche
# ******************************
class Approach(Thread)
    
    def __init__(self, bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')

        self.measured_distance = -1
        self.magnet_detected = -1
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

        self.measured_distance = -1
        self.magnet_detected = -1
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
                    self.measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
                    if self.measured_distance <= HOOKING_DIST:
                        self.cpt_us_touch += 1
                        # self.cpt_us_close = 0 ----> Non placé car permet de reculer et d'arriver en dessous de la HOOKING_DIST
                        if self.cpt_us_touch == self.nb_us_touch:
                            self.cpt_us_close = 0
                            self.US_POS = 'touch'
                    elif self.measured_distance > HOOKING_DIST and self.measured_distance <= HOOKING_DIST + 15:
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
                    self.magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                    if self.magnet_detected:
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
# THREAD 5 - Détection d'erreur pendant le remorquage
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
        self.FLAG_US = False
        self.FLAG_US3 = False
        self.FLAG_CM = False
        # Problem source + explanation
        self.Prob = -1
        self.Expl = -1

        print(self.getName(), 'initialized')

    def run(self):

        self.distance_us = -1
        self.distance_us3 = -1
        self.magnet_detected = -1
        self.cpt_us = 0
        self.cpt_us3 = 0
        self.cpt_cm = 0
        self.cpt_multi = 0
        self.limit_us = 3
        self.limit_us3 = 3
        self.limit_cm = 3
        self.limit_multi = 3
        self.FLAG_US = False
        self.FLAG_US3 = False
        self.FLAG_CM = False
        self.Prob = -1
        self.Expl = -1

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
                        self.distance_us = int.from_bytes(msg.data[4:6], byteorder='big')
                        if self.distance_us > LIMIT_DIST:
                            self.cpt_us += 1
                        else: self.cpt_us = 0
                        if self.cpt_us == self.limit_us:
                            self.FLAG_US = True
                            print("Error US - ", time.strftime("%X"))

                    # Données US3
                    self.distance_us3 = VB.US3
                    if self.distance_us3 > LIMIT_DIST:
                        self.cpt_us3 += 1
                    else: self.cpt_us3 = 0
                    if self.cpt_us3 == self.limit_us3:
                        self.FLAG_US3 = True
                        print("Error US3 - ", time.strftime("%X"))

                    # Données CM
                    if msg.arbitration_id == HALL:
                        self.magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                        if self.magnet_detected == 0:
                            self.cpt_cm += 1
                        else: self.cpt_cm = 0
                        if self.cpt_cm == self.limit_cm:
                            self.FLAG_CM = True
                            print("Error CM - ", time.strftime("%X"))

                    # --------------------------------------
                    # PART 2 - Traitement des flag
                    # --------------------------------------
                    if self.FLAG_CM or self.FLAG_US or self.FLAG_US3:
                        VB.TowingActive.clear()
                        msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
                        self.bus.send(msg)
                        self.cpt_multi += 1

                    # Détermine le message à envoyer en fonction du problème rencontré
                    if self.cpt_multi == self.limit_multi:
                        if self.FLAG_CM and self.FLAG_US and self.FLAG_US3:
                            self.Prob = "CM && US && US3"
                            self.Expl = "Décrochage de la 2e voiture"
                        elif self.FLAG_CM and (self.FLAG_US or self.FLAG_US3):
                            self.Prob = "CM && (US || US3)"
                            self.Expl = "Décrochage de la 2e voiture + capteur US défaillant"
                        elif self.FLAG_CM:
                            self.Prob = "CM"
                            self.Expl = "Capteur magnétique défaillant, 2e voiture toujours accrochée"
                        elif self.FLAG_US and self.FLAG_US3:
                            self.Prob = "US && US3"
                            self.Expl = "Décrochage de la 2e voiture + capteur magnétique défaillant OU barre cassée"
                        elif self.FLAG_US:
                            self.Prob = "US"
                            self.Expl = "US défaillant sur la 1e voiture"
                        elif self.FLAG_US3:
                            self.Prob = "US3"
                            self.Expl = "US défaillant sur la 2e voiture"

                        print("Probleme rencontre: " + self.Prob)


                        # --------------------------------------
                        # PART 3 - Modification des variables à envoyer à l'application et envoi d'un mail d'alerte en cas de panne
                        # --------------------------------------
                   
                        # Ecriture dans la variable "SourceProb" utilisée pour l'envoi du message à l'appli
                        VB.WriteSourceProb(self.Prob)

                        if not(self.FLAG_CM and self.FLAG_US and self.FLAG_US3): # En cas de probleme not corrigible, envoie un mail et arrete le thread
                            mail_subjet = "Unsolvable problem during towing"
                            mail_body = "Origin of the issue : " + self.Prob + "\nPossible explanation : " + self.Expl
                            os.system(echo mail_body | mail -s mail_subjet teamberlingei@gmail.com)
                            break
                        else: # Sinon, réinitialisation des variables en cas de décrochage normal pour le prochain remorquage
                            self.Prob = -1
                            self.Expl = -1