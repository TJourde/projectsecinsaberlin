# coding: utf-8
from threading import *
import time
import can
import os
import struct
import socket

import VarBerlin_slave as VBS

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

TCP_PORT = 9000
BUFFER_SIZE = 20
WAITING_TIME = 10

# *********************************************************
# THREAD 1 - Connection à la voiture noire
# *********************************************************
class MyComSlave(Thread):
    def __init__(self,bus):
        Thread.__init__(self)
        self.bus = bus
        print(self.getName(), '****** MyComSlave initialized')

    def run(self):

        waiting_connection = False
        addr = ''
        stow = -1
        IpPink = VBS.IpPink
        IpBlack = VBS.IpBlack

        while 1:

            # Procédure de déconnexion en cas d'erreur/demande de déconnexion
            if VBS.ConnectionErrorEvent.is_set():
                print(self.getName(),'Connection problem encountered, closing socket')
                VBS.Connection_ON.clear()
                newsendslave.join()
                newreceiveslave.join()
                stow.shutdown(socket.SHUT_RDWR)
                stow.close()
                addr = ''
                VBS.conn_tow = -1
                waiting_connection = False
                print(self.getName(),'Waiting ', str(WAITING_TIME),' sec before continuing')
                time.sleep(WAITING_TIME)
                VBS.ConnectionErrorEvent.clear()

            # Entre dans cette fonction tant que la voiture noire n'est pas connectée
            if not VBS.Connection_ON.is_set():

                # Check si la voiture rose attend déjà une connexion
                if addr == '' and not waiting_connection:
                    waiting_connection = True
                    try:
                        stow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        stow.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        stow.bind((IpPink,TCP_PORT))
                        stow.listen()
                        print(self.getName(),'Pink car ready to receive connection')
                        VBS.conn_tow, addr = stow.accept()
                        waiting_connection = False
                    except socket.error:
                        VBS.Connection_ON.clear()
                        stow.close()
                        print(self.getName(),'Socket error while receiving connection')
                        break
                        
                # Check si l'adresse connectée est bien celle de la voiture noire, si oui commence l'envoi des données
                elif IpBlack in addr:
                    print(self.getName(),'Connected to Berlin car with address' + repr(addr))
                    VBS.Connection_ON.set()

                    newreceiveslave = MyReceiveSlave(VBS.conn_tow,self.bus)
                    newreceiveslave.start()
                    newsendslave = MySendSlave(VBS.conn_tow,self.bus)
                    newsendslave.start()

                # Si quelqu'un autre que la RPi noire se connecte, le déclare, clôt la connection et se met en attente d'une nouvelle
                elif IpBlack not in addr and addr != '':
                    VBS.Connection_ON.clear()
                    print(self.getName(),'Connected to unknown device, with address ' + repr(addr))
                    print(self.getName(),'Closing communication channel')
                    stow.close()
                    addr = -1

        print(self.getName(),'###### MyComSlave closed')


# *********************************************************
# THREAD 2 - Envoi de message à la voiture noire
# *********************************************************
class MySendSlave(Thread):

    def __init__(self,conn,bus):
        Thread.__init__(self)
        self.bus = bus
        self.conn = conn
        print(self.getName(), '****** MySend initialized')

    def run(self):
        while True :
            msg = self.bus.recv()
            if not VBS.Connection_ON.is_set(): break

            if msg.arbitration_id == US2:
                # ultrason avant centre
                distance_us3 = int.from_bytes(msg.data[4:6], byteorder='big')
                message = "UFC_slave:" + str(distance_us3)+ ";"
                try:
                    size = self.conn.send(message.encode())
                    if size == 0: break
                except (BrokenPipeError,ConnectionResetError):
                    VBS.ConnectionErrorEvent.set()
                    break

        print(self.getName(),'###### MySendSlave closed')

# *********************************************************
# THREAD 3 - Réception de messages depuis la voiture noire
# *********************************************************
class MyReceiveSlave(Thread):
    def __init__(self,conn,bus):
        Thread.__init__(self)
        self.conn = conn
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        print(self.getName(), '****** MyReceive initialized')

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True :
            if not VBS.Connection_ON.is_set():break

            data = self.conn.recv(VBS.BUFFER_SIZE)
            data = str(data)
            data = data[2:len(data)-1]
            data = data.split(';')

            if not data: break

            if 'SHUT_DOWN' in data:
                self.conn.send('SHUT_DOWN;'.encode())
                VBS.ConnectionErrorEvent.set()
                break

        print(self.getName(),'###### MyReceiveSlave closed')