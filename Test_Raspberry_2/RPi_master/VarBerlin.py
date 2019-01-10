# coding: utf-8
from threading import *
import os


#IP of the towed vehicle
global IpBlack
global IpPink

# Looking for IP address to "know" which network is used
IpBlack = os.popen('hostname -I').read() # get chain with '[@IP] \n'
IpBlack = IpBlack[:len(IpBlack)-2] # (suppress ' \n')

# Only correct with the two cars black and pink
if IpBlack == '10.105.0.55': # IOT network
    IpPink = '10.105.0.53'
elif IpBlack == '192.168.137.27': # Berlin network
    IpPink = '192.168.137.12'
    

#Semaphore and variable to transmit front US from 2nd car
global US3Sem
US3Sem = BoundedSemaphore(1)
global US3Dispo
US3Dispo = Event()
US3Dispo.clear()
global US3
US3 = -1

#Semaphore and variable to transmit source of the problem
global ErrorCodeSem
ErrorCodeSem = BoundedSemaphore(1)
global ErrorCode
ErrorCode = 0000

global ErrorUSFail
ErrorUSFail = 0b0001
global ErrorUS3Fail
ErrorUS3Fail = 0b0010
global ErrorMag
ErrorMag = 0b0100
global ErrorLostConnection
ErrorLostConnection = 0b1000


#Signal all stop
global stop_all
stop_all = Event()

#Event for connection to pink car
global TryConnect
TryConnect = Event()
TryConnect.clear()
global ConnectedWithPink
ConnectedWithPink = Event()
ConnectedWithPink.clear()
#Events for approaching and hooking
global TryApproach
TryApproach = Event()
TryApproach.clear()
global ApproachComplete
ApproachComplete = Event()
ApproachComplete.clear()
#Events for towing
global TowingActive
TowingActive = Event()
TowingActive.clear()
global TowingError
TowingError = Event()
TowingError.clear()



# *********************************************************
# FUNCTION 1 - Ecrit la valeur en argument dans la variable "US3" (définie au-dessus)
# *********************************************************
def WriteUS3(dispo, value):
    US3Sem.acquire(True):
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
# FUNCTION 3 - Ecrit la valeur en argument dans la variable "ErrorCode" avec blocage (définie au-dessus)
# *********************************************************
def WriteErrorCode(value):
    ErrorCodeSem.acquire(True):
    ErrorCode = ErrorCode | value
    ErrorCodeSem.release()
