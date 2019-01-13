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

HOOKING_DIST = 30

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
class Approach(Thread):
    
    def __init__(self, bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')

        print(self.getName(), '****** Approach initialized')

    def run(self):

        measured_distance = -1
        magnet_detected = -1
        # Compteurs et valeurs limites
        cpt_us_close = 0
        cpt_us_touch = 0
        cpt_magnet = 0
        nb_us_close = 3
        nb_us_touch = 3
        nb_magnet_detection = 3
        # Flag US/Magnet
        US_POS = 'away' # valeur: away | close | touch
        FLAG_MAGNET = False

        while True:

            if VB.stop_all.is_set():break
            
            msg = self.bus.recv()
            
            # Check si l'utilisateur demande la manoeuvre d'approche/accroche du 2e véhicule
            if VB.Approach.is_set():
                print("approach")

                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------
                # Données US
                if msg.arbitration_id == US1:
                    measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
                    if measured_distance <= HOOKING_DIST:
                        cpt_us_touch += 1
                        # cpt_us_close = 0 ----> Non placé car permet de reculer et d'arriver en dessous de la HOOKING_DIST
                        if cpt_us_touch == nb_us_touch:
                            cpt_us_close = 0
                            US_POS = 'touch'
                    elif measured_distance > HOOKING_DIST and measured_distance <= HOOKING_DIST + 15:
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
                        FLAG_MAGNET = False
                    if cpt_magnet == nb_magnet_detection:
                        FLAG_MAGNET = True

                # --------------------------------------
                # PART 2 - Traitement des flag et envoi des commandes aux moteurs/solenoid
                # --------------------------------------
                if US_POS == 'touch' and FLAG_MAGNET:
                    msg = can.Message(arbitration_id=MCM,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    self.bus.send(msg)
                    time.sleep(1)
                    self.msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    bus.send(msg)
                    VB.Hooking_ON.set()
                    VB.Approach.clear()
                elif US_POS == 'touch' and not(FLAG_MAGNET):
                    print(self.getName(),'Alignment error')
                elif US_POS != 'touch' and FLAG_MAGNET:
                    print(self.getName(),'Distance detection error')
                elif US_POS == 'close':
                    print(self.getName(),'Slowing down and opening solenoid')
                    msg = can.Message(arbitration_id=MCM,data=[BACKING_SLOW,BACKING_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                    self.bus.send(msg)
                elif US_POS == 'away':
                    print(self.getName(),'Car away, backing in progress')
                    msg = can.Message(arbitration_id=MCM,data=[BACKING_FAST,BACKING_FAST,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                    self.bus.send(msg)



# ******************************
# THREAD 5 - Détection d'erreur pendant le remorquage
# ******************************
class ErrorDetection(Thread):

    def __init__(self, bus):
        Thread.__init__(self)
        self.bus = bus

        print(self.getName(), '****** ErrorDetection initialized')

    def run(self):

        trame = False
        # Valeurs données
        distance_us = -1
        distance_us3 = -1
        magnet_detected = -1
        # Compteurs
        cpt_us = 0
        cpt_us3 = 0
        cpt_cm = 0
        cpt_multi = 0
        # Valeurs limites
        limit_us = 3
        limit_us3 = 3
        limit_cm = 3
        limit_multi = 3
        # Flag US/Magnet
        FLAG_US = False
        FLAG_US3 = False
        FLAG_CM = False
        # Code d'erreur
        CodeErreur = 0

        while True:
            
            if VB.stop_all.is_set():break
            
            msg = self.bus.recv()
            
            # Check si l'utilisateur demande l'activation du remorquage (donc du mode détection d'erreurs)
            if VB.Towing_ON.is_set():

                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------

                # Données US
                if msg.arbitration_id == US1:
                    trame = True
                    distance_us = int.from_bytes(msg.data[4:6], byteorder='big')
                    if distance_us > LIMIT_DIST:
                        cpt_us += 1
                    else: cpt_us = 0
                    if cpt_us == limit_us:
                        FLAG_US = True
                        print("Error US - ", time.strftime("%X"))

                # Données US3
                if VB.US3Dispo.is_set():
                    distance_us3 = VB.ReadUS3()
                    trame = True
                    if distance_us3 > LIMIT_DIST:
                        cpt_us3 += 1
                    else: cpt_us3 = 0
                    if cpt_us3 == limit_us3:
                        FLAG_US3 = True
                        print("Error US3 - ", time.strftime("%X"))

                # Données CM
                if msg.arbitration_id == HALL:
                    trame = True
                    magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                    if magnet_detected == 0:
                        cpt_cm += 1
                    else: cpt_cm = 0
                    if cpt_cm == limit_cm:
                        FLAG_CM = True
                        print("Error CM - ", time.strftime("%X"))


                if trame and (FLAG_CM or FLAG_US or FLAG_US3):
                    trame = False
                    cpt_multi += 1

                if cpt_multi == limit_multi:
                    VB.Towing_Error.set()

            # --------------------------------------
            # PART 2 - Traitement des flag & envoi d'un mail en cas de panne
            # --------------------------------------
            if VB.Towing_Error.is_set():
                VB.Towing_ON.clear()
                msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
                self.bus.send(msg)

                # Détermine code erreur et l'écrit dans VB.ErrorCode
                if FLAG_US:
                    CodeErreur = CodeErreur | VB.ErrorUSFail
                if FLAG_US3:
                    CodeErreur = CodeErreur | VB.ErrorUS3Fail
                if FLAG_CM:
                    CodeErreur = CodeErreur | VB.ErrorMagFail

                WriteErrorCode(CodeErreur)

                mail_subject = 'Towing process'
                mail_body = 'Error while towing - code: ' + str(CodeErreur)
                print(self.getName(),mail_body)

                if FLAG_CM and FLAG_US and FLAG_US3:
                    print(self.getName(),'Décrochage de la 2e voiture détecté')
                    CodeErreur = 0
                else:                        
                    VB.SendMail(mail_subject, mail_body)
                    break

'''
                    # Détermine le message à envoyer en fonction du problème rencontré
                    if FLAG_CM and FLAG_US and FLAG_US3:
                        Prob = "CM && US && US3"
                        Expl = "Décrochage de la 2e voiture"
                    elif FLAG_CM and FLAG_US:
                        Prob = "CM && US"
                        Expl = "Décrochage de la 2e voiture + capteur US défaillant"
                    elif FLAG_CM and FLAG_US3:
                        Prob = "CM && US3"
                        Expl = "Décrochage de la 2e voiture + capteur US3 (rose) défaillant"
                    elif FLAG_CM:
                        Prob = "CM"
                        Expl = "Capteur magnétique défaillant, 2e voiture toujours accrochée"
                    elif FLAG_US and FLAG_US3:
                        Prob = "US && US3"
                        Expl = "Décrochage de la 2e voiture + capteur magnétique défaillant OU barre cassée"
                    elif FLAG_US:
                        Prob = "US"
                        Expl = "US défaillant sur la 1e voiture"
                    elif FLAG_US3:
                        Prob = "US3"
                        Expl = "US défaillant sur la 2e voiture"

                    print("Code erreur: " + CodeErreur)
                    print("Probleme rencontre: " + Prob)


               
                    # Ecriture dans la variable "SourceProb" utilisée pour l'envoi du message à l'appli

                    if not(FLAG_CM and FLAG_US and FLAG_US3): # En cas de probleme not corrigible, envoie un mail et arrete le thread
                        mail_subjet = "Unsolvable problem during towing"
                        mail_body = "Origin of the issue : " + Prob + "\nPossible explanation : " + Expl
                        os.system("echo mail_body | mail -s mail_subjet teamberlingei@gmail.com")
                        break
                    else: # Sinon, réinitialisation des variables en cas de décrochage normal pour le prochain remorquage
                        CodeErreur = -1
                        Prob = -1
                        Expl = -1
'''
