# coding: utf-8
from threading import *


#IP of the towed vehicle
global IpBlack
global IpPink

# Looking for IP address to "know" which network is used
IpBlack = os.popen('hostname -I').read() # get chain with '[@IP] \n'
IpBlack = IpBlack[:len(IpBlack)-2] # (suppress ' \n')

# Only correct with the two cars black and pink
if IpBlack == '10.105.0.55': # IOT network
    VB.IpRose = '10.105.0.53'
elif IpBlack == '192.168.137.201': # Berlin network
    VB.IpRose = '192.168.137.12'


#Communication variables
global conn
global addr

#Semaphore and variable to transmit front US from 2nd car
global US3Sem
US3Sem = BoundedSemaphore(1)
global US3Dispo
US3Dispo = False
global US3
US3 = -1

#Semaphore and variable to transmit source of the problem
global CodeSem
CodeSem = BoundedSemaphore(1)
global CodeErreur
CodeErreur = ''

#Signal all stop
global stop_all
stop_all = Event()

#Event for connection to pink car
global TryConnect
TryConnect = Event()
TryConnect.clear()
global ConnectComplete
ConnectComplete = Event()
ConnectComplete.clear()
#Events for approaching and hooking
global Approach
Approach = Event()
Approach.clear()
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
async def WriteUS3(dispo, value):
    await US3Sem.acquire()
    US3Dispo = dispo
    US3 = value
    US3.release() # release the semaphore because no longer needed


# *********************************************************
# FUNCTION 2 - Retourne True si variable US3 disponible
# *********************************************************
async def US3Dispo():
    await US3Sem.acquire()
    Dispo = US3Dispo
    US3Sem.release()
    return Dispo


# *********************************************************
# FUNCTION 3 - Retourne la valeur contenue dans US3 (suppose qu'une valeur est dispo)
# *********************************************************
async def ReadUS3():
    await US3Sem.acquire()
    USpink = US3
    US3Dispo = False
    US3Sem.release()
    return USpink


# *********************************************************
# FUNCTION 4 - Ecrit la valeur en argument dans la variable "SourceProb" avec blocage (définie au-dessus)
# *********************************************************
async def WriteSourceProb(value):
    await ProbSem.acquire()
    SourceProb = value
    ProbSem.release()