# coding: utf-8
from threading import *
import os

global BUFFER_SIZE
BUFFER_SIZE = 1024 # standard buffer size


# *********************************************************
# VARIABLE - connexion voiture rose
# *********************************************************
global IpBlack
global IpPink

IpBlack = os.popen('hostname -I').read() #get chain with '[@IP] \n'
IpBlack = IpBlack[:len(IpBlack)-2] #(suppress ' \n')

try:
    IpBlack, MACAddr = IpBlack.split(' ') # remove MAC address appended
except ValueError:
    pass

if '10.105.0.55' in IpBlack: # IOT network
    IpBlack = '10.105.0.55'
    IpPink = '10.105.0.53'
elif '192.168.137.27' in IpBlack: # Berlin network
    IpBlack = '192.168.137.27'
    IpPink = '192.168.137.135'
elif '192.168.1.20' in IpBlack: # Grenier network
    IpBlack = '192.168.1.20'
    IpPink = '192.168.1.21'
elif '192.168.137.41' in IpBlack:
	IpPink = '192.168.137.44'
	IpBlack = '192.168.137.41'

print('IpBlack - ', IpBlack)
print('IpPink - ', IpPink)    

#Semaphore and variable to receive and transmit front US from 2nd car
global UFC_slaveSem
UFC_slaveSem = BoundedSemaphore(1)
global UFC_slaveDispo
UFC_slaveDispo = Event()
UFC_slaveDispo.clear()
global UFC_slave
UFC_slave = -1


# *********************************************************
# VARIABLE - communication par mail
# *********************************************************
global SrcAddr
SrcAddr = 'teamberlingei@gmail.com'
global DestAddr
DestAddr = 'teamberlingei@gmail.com'


# *********************************************************
# VARIABLE - code d'erreur
# *********************************************************
#Semaphore and variable to transmit source of the problem
global ErrorCodeSem
ErrorCodeSem = BoundedSemaphore(1)
global ErrorCode
ErrorCode = 0

global CodeErrorURC
CodeErrorURC = 1
global CodeErrorURFC_slave
CodeErrorURFC_slave = 2
global CodeErrorMAG
CodeErrorMAG = 4
global CodeObstacleUFC
CodeObstacleUFC = 8
global CodeObstacleUFL
CodeObstacleUFL = 16
global CodeObstacleUFR
CodeObstacleUFR = 32
global ErrorLostConnection
ErrorLostConnection = 64


# *********************************************************
# VARIABLE - signaux inter-threads
# *********************************************************
#Signal all stop
global stop_all
stop_all = Event()

#Event for connection to pink car
global Connect
Connect = Event()
Connect.clear()
global Connection_ON
Connection_ON = Event()
Connection_ON.clear()
global Disconnect
Disconnect = Event()
Disconnect.clear()
#Events for approaching and hooking
global Approach
Approach = Event()
Approach.clear()
global Hooking_close
Hooking_close = Event()
Hooking_close.clear()
global Hooking_ON
Hooking_ON = Event()
Hooking_ON.clear()
#Events for towing
global Towing_ON
Towing_ON = Event()
Towing_ON.clear()
global Towing_OFF
Towing_OFF = Event()
Towing_OFF.clear()
global Towing_Error
Towing_Error = Event()
Towing_Error.clear()
global Obstacle_Detected
Obstacle_Detected = Event()
Obstacle_Detected.clear()



# *********************************************************
# FUNCTION 1 - Ecrit la valeur en argument dans la variable "UFC_slave" (définie au-dessus)
# *********************************************************
def WriteUFC_slave(dispo, value):
    UFC_slaveSem.acquire(True)
    UFC_slave = value
    UFC_slaveSem.release() # release the semaphore because no longer needed
    UFC_slaveDispo.is_set()


# *********************************************************
# FUNCTION 2 - Retourne la valeur contenue dans UFC_slave (suppose qu'une valeur est dispo)
# *********************************************************
def ReadUFC_slave():
    if UFC_slaveSem.acquire(False):
        USpink = UFC_slave
        UFC_slaveSem.release()
        UFC_slaveDispo.clear()
        return USpink
    return -1


# *********************************************************
# FUNCTION 3 - Ecrit la valeur en argument dans la variable "ErrorCode" (définie au-dessus) avec blocage 
# *********************************************************
def WriteErrorCode(value):
    global ErrorCode
    ErrorCodeSem.acquire(True)
    ErrorCode = ErrorCode | value
    ErrorCodeSem.release()
