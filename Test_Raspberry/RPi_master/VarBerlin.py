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
global TowingActive
TowingActive = Event()
TowingActive.clear()