# coding: utf-8
from threading import *


#IP of the towed vehicle
global IpTowing
IpTowing = "10.105.0.55"
global IpRose
IpRose = "10.105.0.53"


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
CodeErreur = -1

#Signal all stop
global stop_all
stop_all = Event()

#Event for automatic towing
global Connect
Connect = Event()
Connect.clear()
global Approach
Approach = Event()
Approach.clear()
global ApproachComplete
ApproachComplete = Event()
ApproachComplete.clear()
global TowingActive
TowingActive = Event()
TowingActive.clear()



# *********************************************************
# FUNCTION 1 - Ecrit la valeur en argument dans la variable "US3" (définie au-dessus)
# *********************************************************
def WriteUS3(dispo, value):
    await US3Sem.acquire(False):
    US3Dispo = dispo
    US3 = value
    US3.release() # release the semaphore because no longer needed


# *********************************************************
# FUNCTION 2 - Retourne True si variable US3 disponible
# *********************************************************
def US3Dispo()
    await US3Sem.acquire(False)
    Dispo = US3Dispo
    US3Sem.release()
    return Dispo


# *********************************************************
# FUNCTION 3 - Retourne la valeur contenue dans US3 (suppose qu'une valeur est dispo)
# *********************************************************
def ReadUS3()
    await US3Sem.acquire(False)
    USpink = US3
    US3Dispo = False
    US3Sem.release()
    return USpink


# *********************************************************
# FUNCTION 4 - Ecrit la valeur en argument dans la variable "SourceProb" avec blocage (définie au-dessus)
# *********************************************************
def WriteSourceProb(value):
    await ProbSem.acquire(False)
    SourceProb = value
    ProbSem.release()