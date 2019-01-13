# coding: utf-8
from threading import *
import os


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
if IpBlack == '10.105.0.53': # IOT network
    IpPink = '10.105.0.55'
elif IpBlack == '192.168.137.12': # Berlin network
    IpPink = '192.168.137.27'
elif IpBlack == '192.168.1.21': # Grenier network
    IpPink = '192.168.1.20'

print('IpBlack - ' + IpBlack)
print('IpPink - ' + IpPink)    

#Semaphore and variable to transmit front US from 2nd car
global US3Sem
US3Sem = BoundedSemaphore(1)
global US3Dispo
US3Dispo = Event()
US3Dispo.clear()
global US3
US3 = -1


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
ErrorCode = 0000

global ErrorUSFail
ErrorUSFail = 0b0001
global ErrorUS3Fail
ErrorUS3Fail = 0b0010
global ErrorMagFail
ErrorMag = 0b0100
global ErrorLostConnection
ErrorLostConnection = 0b1000


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



# *********************************************************
# FUNCTION 1 - Ecrit la valeur en argument dans la variable "US3" (définie au-dessus)
# *********************************************************
def WriteUS3(dispo, value):
    US3Sem.acquire(True)
    US3 = value
    US3Sem.release() # release the semaphore because no longer needed
    US3Dispo.is_set()


# *********************************************************
# FUNCTION 2 - Retourne la valeur contenue dans US3 (suppose qu'une valeur est dispo)
# *********************************************************
def ReadUS3():
    if US3Sem.acquire(False):
        USpink = US3
        US3Sem.release()
        US3Dispo.clear()
        return USpink
    return -1


# *********************************************************
# FUNCTION 3 - Ecrit la valeur en argument dans la variable "ErrorCode" (définie au-dessus) avec blocage 
# *********************************************************
def WriteErrorCode(value):
    ErrorCodeSem.acquire(True)
    ErrorCode = ErrorCode | value
    ErrorCodeSem.release()
