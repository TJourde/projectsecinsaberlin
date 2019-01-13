# coding: utf-8
from threading import Thread
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

# *********************************************************
# THREAD 1 - Connection à la voiture noire
# *********************************************************
class MyComSlave(Thread):
    def __init__(self,bus):
        Thread.__init__(self)
        self.bus = bus
        print(self.getName(), 'MyComSlave initialized')

    def run(self):

        waiting_connection = False
        addr = -1
        IpPink = VBS.IpPink
        IpBlack = VBS.IpBlack

        while 1:
            if VBS.ConnectionErrorEvent.is_set():
                print('BrokenPipeError encountered')
                VBS.Connection_ON.clear()
                newsendslave.join()
                newreceiveslave.join()
                del(newsendslave)
                del(newreceiveslave)
                #stow.shutdown()
                stow.close()
                stow = -1
                addr = -1
                VBS.conn_tow = -1
                print('Waiting 15 sec before continuing')
                time.sleep(15)
                VBS.ConnectionErrorEvent.clear()

            if not VBS.Connection_ON.is_set():
                if addr == -1 and not waiting_connection:
                    waiting_connection = True
                    try:
                        stow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        stow.bind((IpPink,TCP_PORT))
                        stow.listen()
                        print('Pink car ready to receive connection')
                        VBS.conn_tow, addr = stow.accept()
                    except socket.error:
                        VBS.Connection_ON.clear()
                        stow.close()
                        print('Socket error while receiving connection')
                        
                # Check si l'adresse connectée est bien celle de la voiture noire, si oui commence l'envoi des données
                elif IpBlack in addr:
                    waiting_connection = False
                    print('Connected to Berlin car with address' + repr(addr))
                    VBS.Connection_ON.set()

                    newreceiveslave = MyReceiveSlave(self.bus)
                    newreceiveslave.start()
                    newsendslave = MySendSlave(VBS.conn_tow,self.bus)
                    newsendslave.start()


                # Si quelqu'un autre que la RPi noire se connecte, le déclare, clôt la connection et se met en attente d'une nouvelle
                elif IpBlack not in addr and addr != -1:
                    waiting_connection = False
                    VBS.Connection_ON.clear()
                    print('Connected to unknown device, with address ' + repr(addr))
                    print('Closing communication channel')
                    stow.close()
                    addr = -1

        print('exit MyComSlave')


# *********************************************************
# THREAD 2 - Envoi de message à la voiture noire
# *********************************************************
class MySendSlave(Thread):

    def __init__(self,conn,bus):
        Thread.__init__(self)
        self.bus = bus
        self.conn = conn
        print(self.getName(), 'MySend initialized')

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

        print('exit MySendSlave')

# *********************************************************
# THREAD 3 - Réception de messages depuis la voiture noire
# *********************************************************
class MyReceiveSlave(Thread):
    def __init__(self,bus):
        Thread.__init__(self)
        self.bus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0
        print(self.getName(), 'MyReceive initialized')

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True :
            if not VBS.Connection_ON.is_set():break
            pass
        print('exit MyReceiveSlave')