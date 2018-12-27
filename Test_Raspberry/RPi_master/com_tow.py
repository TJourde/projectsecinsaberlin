# coding: utf-8

from threading import *
import socket
import struct

#importing variables linked
import VarBerlin as VB


TCP_PORT = 9052
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

# Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
class MyTowCom(Thread)
    
    def __init__(self,IpAddr):
        Thread.__init__(self)
        print(self.getName(), 'initialized')
        self.conn_tow = -1
        self.addr_tow = -1
        self.waiting_connection = False
        self.connected = False

    def run(self):

        while True :

            # Check si l'utilisateur demande l'activation du mode TOWING
            if (VB.Connect.IsSet()):

                # Check si aucune connection n'est en cours
                if ((self.addr_tow == -1) and (self.waiting_connection == False)):
                    waiting_connection = True
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.bind((VB.IpTowing, TCP_PORT))
                        s.listen()
                        self.conn_tow, self.addr_tow = s.accept()
                    except socket.error
                        print('Socket error while attempting to connect to second car')

                # Check si l'adresse connectée est bien celle de la voiture rose, si oui récupère et transmet les données US 
                elif (self.addr_tow == VB.IpRose):
                    self.waiting_connection = False
                    print('Connected to second car with address' + repr(self.addr_tow))

                    data = self.conn.recv(BUFFER_SIZE)
                    if not data:
                        print("No data: lost connection with second car")

                    if "UFC_slave" in data.decode("utf-8"): # look for the identifier in received msg
                        if VN.US3Sem.acquire(False): # acquire semaphore without blocking
                            data = str(data)
                            data = data[2:len(data)-1]
                            data = data.split(';')
                            header_slave, payload_slave = data.split(':')

                            # retrieve message
                            US3 = int(payload_slave)
                            VN.US3.release() # release the semaphore because no longer needed

                            # send it to main application
                            message = "UFC_slave:" + str(playload_slave) + ";"
                            size = self.conn.send(message.encode())
                            if size == 0: 
                                break
                                print(self.getName(),': error while sending data to main application')
                        else:
                            print(self.getName(), ': conflict with another protocol, can not access front US of second car')


                # Si une quelqu'un d'autre que la RPi rose se connecte, le déclare, clôt la connection et se met en attente d'une nouvelle connection
                elif (self.addr_tow != VB.IpRose):
                    self.waiting_connection = True
                    print('Connected to unknown device, with address ' + repr(self.addr_tow))
                    print('Closing communication channel with this address')
                    self.conn_tow.close()
                    self.addr_tow = -1

            # Si le mode TOWING est desactivé et qu'une connection est en cours, clôture de la connection
            elif (not(VB.Connect.IsSet()) and (addr_tow != -1)):
                if (addr_tow == VB.IpRose):
                    print('Towing mode OFF, ', self.getName(), ' closing connection with second car')
                else: print('Towing mode OFF, ', self.getName(), ' closing connection with unknown user')
                self.conn_tow.close()
                self.addr_tow = -1