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
global US3
US3 = -1

#Semaphore and variable to transmit source of the problem
global ProbSem
ProbSem = BoundedSemaphore(1)
global SourceProb
SourceProb = -1

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
def WriteUS3(protocol, value):
    if US3Sem.acquire(False):
        US3 = value
        US3.release() # release the semaphore because no longer needed
    else:
        print(protocol.getName(), ': conflict with another protocol, can not access front US of second car')


# *********************************************************
# FUNCTION 2 - Ecrit la valeur en argument dans la variable "SourceProb" avec blocage (définie au-dessus)
# *********************************************************
def WriteSourceProb(value):
	await ProbSem.acquire()
	SourceProb = value
	ProbSem.release()