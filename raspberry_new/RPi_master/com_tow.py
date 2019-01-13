# coding: utf-8

from threading import *
import socket
import struct
import smtplib

#importing variables linked
import VarBerlin as VB

TCP_PORT = 9000
BUFFER_SIZE = 20  # Normally 1024, but we want fast response


# *********************************************************
# THREAD 3 - Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
# *********************************************************

class MyComTow(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        print(self.getName(), ' - MyTowCom initialized')
        self.conn_tow = -1
        self.addr_tow = -1
        self.connected = False

    def run(self):
        VB.WriteUS3(False,-1)
        while True :
            
            if VB.stop_all.is_set() :
                stow.close()
                break
            
            # --------------------------------------
            # PART 1 - Connexion à la voiture rose
            # --------------------------------------
            if VB.Connect.is_set():
                try:
                    stow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    stow.connect((VB.IpPink,TCP_PORT))
                    print(self.getName(),': Connect to pink car with address ' + VB.IpPink)
                    VB.Connect.clear()
                    VB.Connection_ON.set()
                except socket.error:
                    print(self.getName(),': Socket error while attempting to connect to pink car')
                    VB.Connection_ON.clear()
                    VB.Connect.clear()

            # --------------------------------------
            # PART 2 - Traitement des données envoyées par la voiture rose
            # --------------------------------------
            elif VB.Connection_ON.is_set():

                data = stow.recv(BUFFER_SIZE)

                if not data:
                    print(self.getName(),': No data: lost connection with second car')
                    VB.WriteUS3(False,-1)
                    VB.Connection_ON.clear()
                    VB.Towing_Error.set()
                    VB.WriteErrorCode(VB.ErrorLostConnection)

                # look for the identifier in received msg
                if "UFC_slave" in data.decode("utf-8"): 
                        data = str(data)
                        #data = data[2:len(data)-1]
                        data = data.split(';')
                        header_slave, payload_slave = data.split(':')

                        VB.WriteUS3(True,payload_slave)

                        # send it to main application
                        message = "UFC_slave:" + str(payload_slave) + ";"
                        size = stow.send(message.encode())
                        if size == 0: 
                            print(self.getName(),': error while sending UFC_slave data to IHM')
                            break

            # --------------------------------------
            # Fermeture du socket si arrêt hooking/towing
            # --------------------------------------
            elif VB.Disconnect.is_set():
                stow.close()
                print(self.getName(),': Connection with pink car close')
                VB.Connection_ON.clear()
                VB.Connect.clear()
        print('Exit :' + self.getName())


# *********************************************************
# FONCTION - envoie un mail avec comme contenu les arguments de la fonctions
# *********************************************************
def SendMail(subject,body):
    mail = smtplib.STMP('smtp.gmail.com',587)
    mail.starttls()
    mail.ehlo()
    mail.login('teamberlingei','teamberlingei2018')

    msg = 'Subject: ' + subject + '\n' + body
    mail.sendmail(VB.SrcAddr,VB.DestAddr,msg)
    mail.quit()
    print('Mail sent to ' + VB.DestAddr + 'with content: ' + body)