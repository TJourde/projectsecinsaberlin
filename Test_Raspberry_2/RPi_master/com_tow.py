# coding: utf-8

from threading import *
import socket
import struct
import asyncio

#importing variables linked
import VarBerlin as VB


TCP_PORT = 9052
BUFFER_SIZE = 20  # Normally 1024, but we want fast response


# *********************************************************
# THREAD 3 - Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
# *********************************************************

class MyTowCom(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        print(self.getName(), 'MyTowCom initialized')
        self.conn_tow = -1
        self.addr_tow = -1
        self.connected = False

    def run(self):
        VB.WriteUS3(False,-1)
        while True :
            
            if VB.stop_all.is_set():break
            
            # Check si l'utilisateur demande l'activation du mode TOWING
            if VB.TryConnect.is_set() and not(VB.ConnectComplete.is_set()):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((VB.IpPink,TCP_PORT))
                    print('Connect to pink car with address ' + VB.IpPink)
                    VB.ConnectComplete.set()
                    VB.TryConnect.clear()
                except socket.error:
                    print('Socket error while attempting to connect to pink car')
                    VB.ConnectComplete.clear()
            # Réception des données et écriture dans variable US3
            #elif not(VB.ConnectComplete.is_set() and VB.TryConnect.is_set() and VB.TowingActive.is_set()):
            #    s.close()
            elif VB.ConnectComplete.is_set():
                data = s.recv(BUFFER_SIZE)
                if not data:
                    print("No data: lost connection with second car")
                    VB.WriteUS3(False,-1)

                if "UFC_slave" in data.decode("utf-8"): # look for the identifier in received msg
                        data = str(data)
                        data = data[2:len(data)-1]
                        data = data.split(';')
                        header_slave, payload_slave = data.split(':')

                        VB.WriteUS3(True,payload_slave)

                        # send it to main application
                        message = "UFC_slave:" + str(payload_slave) + ";"
                        size = s.send(message.encode())
                        if size == 0: 
                            break
                            print(self.getName(),': error while sending data to IHM')
