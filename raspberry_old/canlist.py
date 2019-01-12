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
TCP_PORT = 9052
BUFFER_SIZE = 8  # Normally 1024, but we want fast response

def listen_remote_can(num,delay,q):
    #while True:
    
    #    time.sleep(delay)
    #    print ("v:",LIMIT_DIST) 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen()
    conn, addr = s.accept()
    num = 1
    print ('Connection address:', addr)
    while 1:
        time.sleep(delay)
        data = conn.recv(BUFFER_SIZE)
#        print(data)
        if not data:
            print("no data: lost connection")
            num = 0
            q.put(num)
            break
        if "UFC" in data.decode("utf-8"):
#            print("US2:",data)
            us2 = data.decode("utf-8")
            q.put(us2)
#        print ("received data:", data)
#        print('\n')
        q.put(num)
#        conn.send(data)  # echo
        #conn.close()

def listen_can(num,q):
    flag_us = False
    cpt_us = 0
    flag_cm = False
    cpt_cm = 0
    flag_ufc = False
    cpt_ufc = 0
    ufc = -1
    cpt_both = 0
    #num = 1 #toremove for connection with other car
    tps=time.time()
    log=""
    log2=""
    log3=""
    go = False
    write_log = 0
    while True :
        if not q.empty():
 #           print(q.qsize())
            if q.qsize() > 1:
                us2=q.get()
                num=q.get()
                go = True
                #print(us2)
                if "UFC" in us2:
                    #write_log = 2
                    log+=us2
                    ufc=us2.strip("UFC:")
               #     print(ufc.replace(';',''))
                    ufc=ufc.replace(';','')
                    ufc=int(ufc)
              #      print("ufc:",ufc)
             #   print("us2:",us2)
            else:
                num=q.get()
                print("lost connection")
                #print(num)
            
#        else:
#            print('non')
        trame=False
        
        #msg = bus.recv()
        if go :
#            print('hi')
            msg = bus.recv()

            #print(msg.arbitration_id, msg.data)
            st = ""

            if msg.arbitration_id == US1:
                # ultrason avant gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "UFL:" + str(distance) + ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason avant droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "UFR:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason arriere centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "URC:" + str(distance)+ ";"
                #if write_log == 2 :
                log2+=message
                #    write_log = write_log - 1
                #size = self.conn.send(message.encode())
                #if size == 0: break
            elif msg.arbitration_id == US2:
                # ultrason arriere gauche
                distance = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "URL:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason arriere droit
                distance = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "URR:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # ultrason avant centre
                distance = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "UFC:" + str(distance)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
            elif msg.arbitration_id == MS:
                # position volant
                angle = int.from_bytes(msg.data[0:2], byteorder='big')
                message = "POS:" + str(angle)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # Niveau de la batterie
                bat = int.from_bytes(msg.data[2:4], byteorder='big')
                message = "BAT:" + str(bat)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # vitesse roue gauche
                speed_left = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "SWL:" + str(speed_left)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # vitesse roue droite
                # header : SWR payload : entier, *0.01rpm
                speed_right= int.from_bytes(msg.data[6:8], byteorder='big')
                message = "SWR:" + str(speed_right)+ ";"
                #size = self.conn.send(message.encode())
                #if size == 0: break
            elif msg.arbitration_id == OM1:
                # Yaw
                yaw = struct.unpack('>f',msg.data[0:4])
                message = "YAW:" + str(yaw[0])+ ";"
                #print(message)
                #st += message
                #size = self.conn.send(message.encode())
                #if size == 0: break
                # Pitch
                pitch = struct.unpack('>f',msg.data[4:8])
                message = "PIT:" + str(pitch[0])+ ";"
                #print(message)
                #st += message
                #size = self.conn.send(message.encode())
                #if size == 0: break
            elif msg.arbitration_id == OM2:
                # Roll
                roll = struct.unpack('>f',msg.data[0:4])
                message = "ROL:" + str(roll[0])+ ";"
                #print(message)
                #st += message
                #   size = self.conn.send(message.encode())
                #if size == 0: break
            elif msg.arbitration_id == Hall:
                trame = True
                magnet=int.from_bytes(msg.data[0:1],byteorder='big')
                message = "CM:"+ str(magnet)+";"
                #print(message)
                #if write_log == 1 :
                log3+=message
                #    write_log = write_log - 1
                
            
            tps2 = time.time()
            print(tps2-tps)
            if tps2-tps>=15 :
                print(log)
                print(log2)
                print(log3)
                exit()
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

threads = []
#msg = can.Message(arbitration_id=0x010,data=[0xBC, 0xBC, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
#bus.send(msg)

try:
    q = queue.Queue()
    connected = -1
    t = Thread(target=listen_can,args=(connected,q),daemon=True)
    threads.append(t)
    t.start()

    t = Thread(target=listen_remote_can,args=(connected,2,q),daemon=True)
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
