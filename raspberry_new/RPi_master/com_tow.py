# coding: utf-8

from threading import *
import socket
import struct
import smtplib

#importing variables linked
import VarBerlin as VB

TCP_PORT = 9052
BUFFER_SIZE = 20  # Normally 1024, but we want fast response


# *********************************************************
# THREAD 3 - Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
# *********************************************************

class MyComTow(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        print(self.getName(), 'MyTowCom initialized')
        self.conn_tow = -1
        self.addr_tow = -1
        self.connected = False

    def run(self):
        VB.WriteUS3(False,-1)
        while True :
            
            if VB.stop_all.is_set():
                break
                s.close()
            
            # --------------------------------------
            # PART 1 - Essai de connexion à la voiture rose
            # --------------------------------------

            if VB.TryConnect.is_set():
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((VB.IpPink,TCP_PORT))
                    print('Connect to pink car with address ' + VB.IpPink)
                    VB.ConnectedWithPink.set()
                    VB.TryConnect.clear()
                except socket.error:
                    print('Socket error while attempting to connect to pink car')
                    VB.ConnectedWithPink.clear()
                    VB.TryConnect.clear()

            # --------------------------------------
            # PART 2 - Traitement des données envoyées par la voiture rose
            # --------------------------------------

            # Réception des données et écriture dans variable US3
            elif VB.ConnectedWithPink.is_set():

                data = s.recv(BUFFER_SIZE)
                if not data:
                    print("No data: lost connection with second car")
                    VB.WriteUS3(False,-1)
                    VB.ConnectedWithPink.clear()
                    VB.TowingError.set()
                    VB.WriteErrorCode(VB.ErrorLostConnection)

                # look for the identifier in received msg
                if "UFC_slave" in data.decode("utf-8"): 
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
                            print(self.getName(),': error while sending UFC_slave data to IHM')



# *********************************************************
# FONCTION - envoie un mail avec comme contenu les arguments de la fonctions
# *********************************************************
def SendMail(subject,body):
    mail = smtplib.STMP('smtp.gmail.com',587)
    s.starttls()
    s.ehlo()
    s.login('teamberlingei','teamberlingei2018')

    msg = 'Subject: ' + subject + '\n' + body
    mail.sendmail(VB.SrcAddr,VB.DestAddr,msg)
    mail.quit()
    print('Mail sent to ' + VB.DestAddr + 'with content: ' + body)