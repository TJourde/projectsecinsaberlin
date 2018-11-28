# coding: utf-8
from threading import Thread
import queue
import time
import can
import os
import struct
import socket
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

LIMIT_DIST = 35

TCP_IP = '10.105.0.55'
TCP_PORT = 9050
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

def listen_remote_can(num,delay,q):
    #while True:
    
    #    time.sleep(delay)
    #    print ("v:",LIMIT_DIST) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    conn, addr = s.accept()
    num = 1
    print ('Connection address:', addr)
    while 1:
        time.sleep(delay)
        data = conn.recv(BUFFER_SIZE)
        if not data:
            num = 0
            q.put(num)
            break
        print ("received data:", data)
        print('\n')
        q.put(num)
        #conn.send(data)  # echo
        #conn.close()

def listen_can(num,q):
    flag_us = False
    cpt_us = 0
    flag_cm = False
    cpt_cm = 0
    
    cpt_both = 0
    num = 1 #toremove for connection with other car
    
    while True :
        if not q.empty():
            print('oui')
            num=q.get_nowait()
        else:
            print('non')
        trame=False
        msg = bus.recv()
        
        if msg.arbitration_id == US1:
            trame = True
# ultrason arriere centre
            distance = int.from_bytes(msg.data[4:6], byteorder='big')
            message = "URC:" + str(distance)+ ";"
#            print(message)
            if distance > LIMIT_DIST:
                cpt_us += 1
                if cpt_us > 2:
                    flag_us = True
#                    print('Car gone: décrochage détecté\n')
                    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
                    bus.send(msg)
            elif distance <= LIMIT_DIST:
                cpt_us = 0
#                print('OK\n')
        elif msg.arbitration_id == Hall:
            trame = True
            magnet=int.from_bytes(msg.data[0:1],byteorder='big')
#            print(magnet)
            if magnet==0:
                cpt_cm += 1
                if cpt_cm > 2:
                    flag_cm = True
                    print('Too Far: décrochage détecté\n')
                    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
                    bus.send(msg)
            elif magnet==1:
                cpt_cm = 0
#                print("attache")

        if num==0:
            print('Lost connexion with remote car: décrochage détecté\n')
            msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
            bus.send(msg)
        if trame:
            if flag_cm or flag_us:
                cpt_both += 1
                if cpt_both > 3:
                    if flag_cm and flag_us:
                        print('CM && US')
                    elif flag_cm:
                        print('CM')
                    elif flag_us:
                        print('US')
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

threads = []

try:
    q = queue.Queue()
    num = 0
    t = Thread(target=listen_can,args=(num,q),daemon=True)
    threads.append(t)
    t.start()

    t = Thread(target=listen_remote_can,args=(num,2,q),daemon=True)
    threads.append(t)
    t.start()
except:
    print ("EROR?.?")
    exit()
    
#        print (message)
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




try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
    bus.send(msg)
    exit()
