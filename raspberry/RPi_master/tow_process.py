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

import com_tow as CT


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

# DISTANCES
HOOKING_DIST = 33
SLOWING_DIST = HOOKING_DIST + 30 # car will slow down approach if under this distance
LIMIT_DIST = HOOKING_DIST + 5
OBSTACLE_DIST = 30

# COMMANDES SOLENOID
SOLENOID_UP = 0xFF
SOLENOID_DOWN = 0x00

# COMMANDES ROUES
NO_MOVE = 0xB1
FORWARD_SLOW = 0xB7
BACKWARD_FAST = 0xA6
BACKWARD_SLOW = 0xAB
WHEELS_CENTER = 0xB1


# ******************************
# THREAD 4 - Procédure d'approche
# ******************************
class Approach(Thread):
    
    def __init__(self, bus):
        Thread.__init__(self)
        self.bus  = bus

        print(self.getName(), '****** Approach initialized')

    def run(self):

        trameCAN = False
        # Données
        distance_URC = -1
        magnet_detected = -1
        # Compteur
        compteur_close = 0
        compteur_touch = 0
        compteur_magnet = 0
        # Valeurs limite
        limit_close = 3
        limit_touch = 3
        limit_magnet = 3
        # Flag
        POSITION = 'away' # valeur: away | close | touch
        FLAG_MAGNET = False

        while True:

            if VB.stop_all.is_set():break
            
            # Check si l'utilisateur demande la manoeuvre d'approche/accroche du 2e véhicule
            if VB.Approach.is_set() or VB.Hooking_close.is_set():

                trameCAN = False
                msg = self.bus.recv()

                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------
                # Données US
                if msg.arbitration_id == US1:
                    trameCAN = True
                    distance_URC = int.from_bytes(msg.data[4:6], byteorder='big')
                    if distance_URC <= HOOKING_DIST:
                        compteur_touch += 1
                        # compteur_close = 0 ----> Non placé car permet de reculer et d'arriver en dessous de la HOOKING_DIST
                        if compteur_touch == limit_touch:
                            compteur_close = 0
                            POSITION = 'touch'
                    elif distance_URC > HOOKING_DIST and distance_URC <= SLOWING_DIST:
                        compteur_touch = 0
                        compteur_close += 1
                        if compteur_close == limit_close:
                            POSITION = 'close'
                    else: 
                        compteur_close = 0
                        compteur_touch = 0
                        POSITION = 'away'

                # Données capteur magnétique
                if msg.arbitration_id == HALL:
                    trameCAN = True
                    magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')
                    if magnet_detected:
                        compteur_magnet += 1
                    else:
                        FLAG_MAGNET = False
                    if compteur_magnet == limit_magnet:
                        FLAG_MAGNET = True

                # --------------------------------------
                # PART 2 - Traitement des flag et envoi des commandes aux moteurs/solenoid
                # --------------------------------------
                if trameCAN:
                    if POSITION == 'touch' and FLAG_MAGNET:
                        print(self.getName(),'Hooking effective')
                        msg = can.Message(arbitration_id=MCM,data=[BACKWARD_SLOW,BACKWARD_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                        self.bus.send(msg)
                        time.sleep(1)
                        msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                        self.bus.send(msg)
                        VB.Approach.clear()
                        VB.Hooking_close.clear()
                        VB.Hooking_ON.set()
                    elif POSITION == 'touch' and not(FLAG_MAGNET):
                        print(self.getName(),'Alignment error')
                        msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                        self.bus.send(msg)
                        VB.Approach.clear()
                        VB.Hooking_close.set()
                    elif POSITION != 'touch' and FLAG_MAGNET:
                        print(self.getName(),'Distance detection error')
                        msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                        self.bus.send(msg)
                        VB.Approach.clear()
                        VB.Hooking_close.set()
                    elif POSITION == 'close':
                        print(self.getName(),'Slowing down and opening solenoid')
                        msg = can.Message(arbitration_id=MCM,data=[BACKWARD_SLOW,BACKWARD_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                        self.bus.send(msg)
                    elif POSITION == 'away':
                        print(self.getName(),'Car away, backing in progress')
                        msg = can.Message(arbitration_id=MCM,data=[BACKWARD_FAST,BACKWARD_FAST,0,WHEELS_CENTER,0,0,0,SOLENOID_DOWN],extended_id=False)
                        self.bus.send(msg)

        print(self.getName(), '###### Approach finished')


# ******************************
# THREAD 5 - Détection d'erreur pendant le remorquage
# ******************************
class TowingErrorDetection(Thread):

    def __init__(self, bus):
        Thread.__init__(self)
        self.bus = bus

        print(self.getName(), '****** ErrorDetection initialized')

    def run(self):

        trameCAN_tow = False
        trameCAN_obs = False
        # Valeurs données
        distance_URC = -1
        distance_UFC_slave = -1
        magnet_detected = -1
        distance_UFC = -1
        distance_UFL = -1
        distance_UFR = -1
        # Compteurs
        compteur_URC = 0
        compteur_UFC_slave = 0
        compteur_MAG = 0
        compteur_multi = 0
        compteur_UFC = 0
        compteur_UFL = 0
        compteur_UFR = 0
        # Valeurs limites
        limit_URC = 10
        limit_UFC_slave = 4
        limit_MAG = 10
        limit_multi = 15
        limit_UFC = 6
        limit_UFL = 6
        limit_UFR = 6
        # Flag US/Magnet
        FLAG_URC = False
        FLAG_UFC_slave = False
        FLAG_MAG = False
        FLAG_UFC = False
        FLAG_UFL = False
        FLAG_UFR = False
        # Code d'erreur
        CodeErreur = 0

        while True:
            
            if VB.stop_all.is_set():break

            msg = self.bus.recv()

            if VB.Towing_OFF.is_set():
                print(self.getName(),'Unhooking procedure initialized')
                VB.Towing_ON.clear()
                VB.Hooking_ON.clear()
                VB.Disconnect.set()
                
                msg = can.Message(arbitration_id=MCM,data=[NO_MOVE,NO_MOVE,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                self.bus.send(msg)
                time.sleep(1)
                msg = can.Message(arbitration_id=MCM,data=[FORWARD_SLOW,FORWARD_SLOW,0,WHEELS_CENTER,0,0,0,SOLENOID_UP],extended_id=False)
                self.bus.send(msg)
            
            # Si le towing est demandé mais que la voiture rose n'est pas connectée
            if VB.Towing_ON.is_set() and not VB.Connection_ON.is_set():
                print(self.getName(),'Not connected to pink car, cancelling towing procedure')
                VB.Towing_ON.clear()

            # Check si l'utilisateur demande l'activation du remorquage (donc du mode détection d'erreurs)
            if VB.Connection_ON.is_set() and VB.Towing_ON.is_set() :
                VB.Hooking_ON.clear()

                # --------------------------------------
                # PART 1 - Traitement des données et levée des flag
                # --------------------------------------
                if msg.arbitration_id == US1:
                    trameCAN_tow = True
                    trameCAN_obs = True
                    distance_UFL = int.from_bytes(msg.data[0:2], byteorder='big')
                    distance_UFR = int.from_bytes(msg.data[2:4], byteorder='big')
                    distance_URC = int.from_bytes(msg.data[4:6], byteorder='big')

                    # UFL data
                    if distance_UFL < OBSTACLE_DIST:
                        compteur_UFL += 1
                    else: compteur_UFL = 0
                    if compteur_UFL == limit_UFL:
                        FLAG_UFL
                        print(self.getName(),'Error UFL - ', time.strftime("%X"))
                    # UFR data
                    if distance_UFR < OBSTACLE_DIST:
                        compteur_UFR += 1
                    else: compteur_UFR = 0
                    if compteur_UFR == limit_UFR:
                        FLAG_UFR
                        print(self.getName(),'Error UFR - ', time.strftime("%X"))
                    # URC data
                    if distance_URC > LIMIT_DIST:
                        compteur_URC += 1
                    else: compteur_URC = 0
                    if compteur_URC == limit_URC:
                        FLAG_URC = True
                        print(self.getName(),'Error URC - ', time.strftime("%X"))


                if msg.arbitration_id == US2:
                    trameCAN_obs = True
                    distance_UFC = int.from_bytes(msg.data[4:6], byteorder='big')

                    # UFC data
                    if distance_UFC < OBSTACLE_DIST:
                        compteur_UFC += 1
                    else: compteur_UFC = 0
                    if compteur_UFC == limit_UFC:
                        FLAG_UFC
                        print(self.getName(),'Error UFC - ', time.strftime("%X"))


                if msg.arbitration_id == HALL:
                    trameCAN_tow = True
                    magnet_detected = int.from_bytes(msg.data[0:1], byteorder='big')

                    # MAG data
                    if magnet_detected == 0:
                        compteur_MAG += 1
                    else: compteur_MAG = 0
                    if compteur_MAG == limit_MAG:
                        FLAG_MAG = True
                        print(self.getName(),'Error MAG - ', time.strftime("%X"))


                if VB.UFC_slaveDispo.is_set():
                    trameCAN_tow = True
                    distance_UFC_slave = VB.ReadUFC_slave()

                    # UFC_slave data
                    if distance_UFC_slave > LIMIT_DIST:
                        compteur_UFC_slave += 1
                    else: compteur_UFC_slave = 0
                    if compteur_UFC_slave == limit_UFC_slave:
                        FLAG_UFC_slave = True
                        print(self.getName(),"Error UFC_slave - ", time.strftime("%X"))


                # --------------------------------------
                # PART 2 - Appel des handler
                # --------------------------------------
                if trameCAN_tow and (FLAG_MAG or FLAG_URC or FLAG_UFC_slave):
                    trameCAN_tow = False
                    compteur_multi += 1
                    if compteur_multi == limit_multi:
                        TowingErrorHandler(self,FLAG_URC,FLAG_UFC_slave,FLAG_MAG)

                if trameCAN_obs and (FLAG_UFC or FLAG_UFL or FLAG_UFR):
                    trameCAN_obs = False
                    ObstacleHandler(self,FLAG_UFC,FLAG_UFL,FLAG_UFR)

        print(self.getName(), '###### TowingErrorDetection finished')
'''
            # --------------------------------------
            # PART 2 - Traitement des flag & envoi d'un mail en cas de panne
            # --------------------------------------
            if VB.Towing_Error.is_set():
                VB.Towing_ON.clear()
                msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
                self.bus.send(msg)

                # Détermine code erreur et l'écrit dans VB.ErrorCode
                if FLAG_URC:
                    CodeErreur = CodeErreur | VB.CodeErrorURC
                if FLAG_UFC_slave:
                    CodeErreur = CodeErreur | VB.ErrorUS3Fail
                if FLAG_CM:
                    CodeErreur = CodeErreur | VB.CodeErrorMAG

                WriteErrorCode(CodeErreur)

                mail_subject = 'Towing process'
                mail_body = 'Error while towing - code: ' + str(CodeErreur)
                print(self.getName(),mail_body)

                if FLAG_CM and FLAG_URC and FLAG_UFC_slave:
                    print(self.getName(),'Décrochage de la 2e voiture détecté')
                    CodeErreur = 0
                else:                        
                    VB.SendMail(mail_subject, mail_body)
                    break


                    # Détermine le message à envoyer en fonction du problème rencontré
                    if FLAG_CM and FLAG_US and FLAG_UFC_slave:
                        Prob = "CM && US && US3"
                        Expl = "Décrochage de la 2e voiture"
                    elif FLAG_CM and FLAG_US:
                        Prob = "CM && US"
                        Expl = "Décrochage de la 2e voiture + capteur US défaillant"
                    elif FLAG_CM and FLAG_UFC_slave:
                        Prob = "CM && US3"
                        Expl = "Décrochage de la 2e voiture + capteur US3 (rose) défaillant"
                    elif FLAG_CM:
                        Prob = "CM"
                        Expl = "Capteur magnétique défaillant, 2e voiture toujours accrochée"
                    elif FLAG_US and FLAG_UFC_slave:
                        Prob = "US && US3"
                        Expl = "Décrochage de la 2e voiture + capteur magnétique défaillant OU barre cassée"
                    elif FLAG_US:
                        Prob = "US"
                        Expl = "US défaillant sur la 1e voiture"
                    elif FLAG_UFC_slave:
                        Prob = "US3"
                        Expl = "US défaillant sur la 2e voiture"

                    print("Code erreur: " + CodeErreur)
                    print("Probleme rencontre: " + Prob)


               
                    # Ecriture dans la variable "SourceProb" utilisée pour l'envoi du message à l'appli

                    if not(FLAG_CM and FLAG_US and FLAG_UFC_slave): # En cas de probleme not corrigible, envoie un mail et arrete le thread
                        mail_subjet = "Unsolvable problem during towing"
                        mail_body = "Origin of the issue : " + Prob + "\nPossible explanation : " + Expl
                        os.system("echo mail_body | mail -s mail_subjet teamberlingei@gmail.com")
                        break
                    else: # Sinon, réinitialisation des variables en cas de décrochage normal pour le prochain remorquage
                        CodeErreur = -1
                        Prob = -1
                        Expl = -1
'''


# ******************************
# FUNCTION - Handler d'erreur pendant remorquage
# ******************************
def TowingErrorHandler(self,FLAG_URC,FLAG_UFC_slave,FLAG_MAG):
    Code_erreur = 0
    msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
    self.bus.send(msg)
    print(self.getName(),'Error while towing')
    VB.Towing_ON.clear()
    VB.Towing_Error.set()
    Code_erreur = VB.CodeErrorURC * int(FLAG_URC == True) + VB.CodeErrorURFC_slave * int(FLAG_UFC_slave == True) + VB.CodeErrorMAG * int(FLAG_MAG == True)
    print(self.getName(),'Exit towing with code ', str(bin(Code_erreur)))
    VB.WriteErrorCode(Code_erreur)
    if FLAG_URC and FLAG_UFC_slave and FLAG_MAG:
        print(self.getName(),'Unhooking detected')
        VB.Hooking_ON.clear()
        time.sleep(3)
        print(self.getName(),'Trying to rehook')
        VB.Approach.is_set()
    else:
        mail_subject = 'Towing process error'
        mail_body = 'Error while towing - code: ' + str(bin(Code_erreur))
        CT.SendMail(mail_subject, mail_body)



# ******************************
# FUNCTION - Handler de détection d'obstacle
# ******************************
def ObstacleHandler(self,FLAG_UFC,FLAG_UFL,FLAG_UFR):
    Code_erreur = 0
    msg = can.Message(arbitration_id=MCM,data=[NO_MOVE, NO_MOVE, 0, WHEELS_CENTER, 0, 0, 0, SOLENOID_DOWN], extended_id=False)
    self.bus.send(msg)
    print(self.getName(),'Obstacle detected')
    VB.Towing_ON.clear()
    VB.Towing_Error.set()
    Code_erreur = VB.CodeObstacleUFC * int(FLAG_UFC == True) + VB.CodeObstacleUFL * int(FLAG_UFL == True) + VB.CodeObstacleUFR * int(FLAG_UFR == True)
    VB.WriteErrorCode(Code_erreur)
    print(self.getName(),'Exit towing with code ', str(bin(Code_erreur)))

