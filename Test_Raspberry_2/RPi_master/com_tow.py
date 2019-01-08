# coding: utf-8

from threading import *
import socket
import struct

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

            # Check si l'utilisateur demande l'activation du mode TOWING
            if TryConnect.is_set() and not(ConnectComplete.is_set()):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((IpPink,TCP_PORT))
                    print('Connect to pink car with address ' + IpPink)
                    ConnectComplete.set()
                    TryConnect.clear()
                except socket.error:
                    print('Socket error while attempting to connect to pink car')
                    ConnectComplete.set()

            # Réception des données et écriture dans variable US3
            if ConnectComplete.is_set():
                data = sock.recv(BUFFER_SIZE)
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
                        size = sock.send(message.encode())
                        if size == 0: 
                            break
                            print(self.getName(),': error while sending data to IHM')
