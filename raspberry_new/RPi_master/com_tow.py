# coding: utf-8

from threading import *
import socket
import struct
import smtplib

#importing variables linked
import VarBerlin as VB

TCP_PORT = 9000


# *********************************************************
# THREAD 3 - Connection à la 2e voiture, récupèration les données envoyées et les transmission à l'appli principale
# *********************************************************

class MyComTow(Thread):
    
    def __init__(self,conn_IHM):
        Thread.__init__(self)
        self.conn_IHM = conn_IHM
        print(self.getName(), '****** MyTowCom initialized')

    def run(self):

        VB.WriteUFC_slave(False,-1)
        while True :
            
            if VB.stop_all.is_set() :
                if VB.Connection_ON.is_set():
                    VB.Disconnect.set()
                else: 
                    break
            
            # --------------------------------------
            # Fermeture du socket (si arrêt hooking/towing)
            # --------------------------------------
            if VB.Disconnect.is_set():
                VB.Connection_ON.clear()
                VB.Connect.clear()
                stow.send('SHUT_DOWN;'.encode())
                while 'SHUT_DOWN' not in data:
                    data = stow.recv(VB.BUFFER_SIZE)
                    data = str(data)
                    data = data[2:len(data)-1]
                    data = data.split(';')
                stow.close()
                print(self.getName(),'Connection with pink car closed')
                VB.Disconnect.clear()

                if VB.stop_all.is_set(): break

            # --------------------------------------
            # Traitement des données envoyées par la voiture rose
            # --------------------------------------
            elif VB.Connection_ON.is_set():

                data = stow.recv(VB.BUFFER_SIZE)
                data = str(data)
                data = data[2:len(data)-1]

                if not data: continue

                for cmd in data.split(';'):

                    #print(self.getName(), cmd)

                    # look for the identifier in received msg
                    if "UFC_slave" in cmd: 

                            header_slave, payload_slave = cmd.split(':')

                            VB.WriteUFC_slave(True,payload_slave)

                            # send it to main application
                            message = "UFC_slave:" + str(payload_slave) + ";"
                            size = self.conn_IHM.send(message.encode())
                            if size == 0: 
                                print(self.getName(),'Error while sending UFC_slave data to IHM')
                                break

            # --------------------------------------
            # Connexion à la voiture rose
            # --------------------------------------
            elif VB.Connect.is_set():
                try:
                    stow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    stow.connect((VB.IpPink,TCP_PORT))
                    print(self.getName(),'Connect to pink car with address ' + VB.IpPink)
                    VB.Connect.clear()
                    VB.Connection_ON.set()
                except socket.error:
                    print(self.getName(),'Socket error while attempting to connect to pink car')
                    VB.Connection_ON.clear()
                    VB.Connect.clear()



        print(self.getName(), '###### MyTowCom finished')


# *********************************************************
# FONCTION - envoie un mail avec comme contenu les arguments de la fonctions
# *********************************************************
def SendMail(subject,body):
    mail = smtplib.SMTP('smtp.gmail.com',587)
    mail.starttls()
    mail.ehlo()
    mail.login('teamberlingei','teamberlin2018')

    msg = 'Subject: ' + subject + '\n' + body
    mail.sendmail(VB.SrcAddr,VB.DestAddr,msg)
    mail.quit()
    print('Mail sent to ' + VB.DestAddr + 'with content: ' + body)