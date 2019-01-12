# coding: utf-8
from threading import Thread
import queue
import time
import can
import os
import struct
import socket
MCM = 0x010 
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102
Hall= 0x103
HALL= 0x103
magnet_detected = 0
measured_distance = 0
LIMIT_DIST = 35
SOLENOID_ON = 0xA0
SOLENOID_OFF = 0x00
HOOKING_DIST =  30
FROM_PI = 0x010
TCP_IP = '10.105.0.55'
TCP_PORT = 9052
BUFFER_SIZE = 8  # Normally 1024, but we want fast response
SAFE_FRONT_DIST = 30   
mode =0 # mode 0 receive info rom app, mode 1 - : mode 2 -  mode 3 -:

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
msg = bus.recv()



#Forward_Driving
def drive_forward():       
    print('Driving Forward') 
    cmd_mv = 0xBB
    cmd_turn = 0xB0
    cmd_pos = 0xB1
    msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
    bus.send(msg)
    while True :
        #Check front range left and right
        #stop if obstacle found
        msg = bus.recv()
        if msg.arbitration_id == US1:
            front_range_left = int.from_bytes(msg.data[0:2], byteorder='big')
            front_range_right = int.from_bytes(msg.data[2:4], byteorder='big')

            #checking obstacles in front
            if front_range_left <= SAFE_FRONT_DIST or front_range_right < SAFE_FRONT_DIST :      
                #stop()
                print('Front Range Left :',  front_range_left)
                print('Front Range Right :', front_range_right)
            else:
                print('Driving Forward!')
                cmd_mv = 0xBB
                cmd_turn = 0xB1
                cmd_pos = 0xB1

                #check straightness
                if front_range_left < front_range_right  + 10 :
                    cmd_pos = 0xE3
                    cmd_pos = 0xE3
                elif front_range_left > front_range_right + 10 :
                    cmd_pos = 0x80
                    cmd_turn = 0x80
                else: 
                    cmd_turn = 0xB1
                    cmd_pos  = 0xB1
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
                bus.send(msg)   
       
        # check direct front range
        elif msg.arbitration_id == US2:
            front_range = int.from_bytes(msg.data[4:6], byteorder='big')
            print('Front Range :', front_range)
            if front_range <= SAFE_FRONT_DIST :
                stop()
            else:
                print('Driving Forward!')
                cmd_mv = 0xBB
                cmd_turn = 0xB1  
                # check straightness
                if front_range_left < front_range_right  + 10 :
                    cmd_pos = 0xE3
                    cmd_pos = 0xE3
                elif front_range_left > front_range_right + 10 :
                    cmd_pos = 0x80
                    cmd_turn = 0x80
                else: 
                    cmd_turn = 0xB1
                    cmd_pos  = 0xB1
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
                bus.send(msg)  
#Backward driving
def drive_backwards():
    print('Backing in progress') 
    cmd_mv_l = 0xAB
    cmd_mv_r = 0xAB
    cmd_turn = 0xB0
    cmd_pos =  0xB1
    msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
    bus.send(msg)  
    while True :
        msg = bus.recv()
        if msg.arbitration_id == US1:
            measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
            print('measured distance : ', measured_distance)
            if measured_distance <  HOOKING_DIST + 15 and  measured_distance >  HOOKING_DIST :
                print('slowing down')
                cmd_mv -= 1 
                cmd_turn = 0xB0
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
                bus.send(msg)
                print('opening solenoid')
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,SOLENOID_ON],extended_id=False)
                bus.send(msg)      
            else:
                print('Backing in progress')
                cmd_mv = 0xAB
                cmd_turn = 0xB0
                cmd_pos = 0xB1
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
                bus.send(msg)

        elif msg.arbitration_id == US2:
            # ultrason arriere gauche
            left_distance = int.from_bytes(msg.data[0:2], byteorder='big')
            # ultrason arriere droit
            right_distance = int.from_bytes(msg.data[2:4], byteorder='big')
            if right_distance < left_distance + 0.5 :
                cmd_pos = 0xE3
            elif right_distance > left_distance + 0.5 :
                cmd_pos = 0x80
            else: 
                cmd_pos = 0xB1                 

#drive backwards 
#hook the vehicle when at right distance
#test hooking effectiveness and rehook if necessary
def hook():
    while True :
        #measure ultrason arriere centre
        msg = bus.recv()
        if msg.arbitration_id == US1:
            measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
            print('measured distance : ', measured_distance)
            
            if measured_distance <  HOOKING_DIST + 15 and  measured_distance >  HOOKING_DIST :
                print('slowing down')
                cmd_mv = 0xAD 
                cmd_turn = 0xB0
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
                bus.send(msg)
                print('opening solenoid')
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,SOLENOID_ON],extended_id=False)
                bus.send(msg)      
            else:
                print('Backing in progress')
                cmd_mv = 0xA0
                cmd_turn = 0xB0
                cmd_pos = 0xB1
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
                bus.send(msg)

            if measured_distance <= HOOKING_DIST and magnet_detected :
                #stop backing 
                #close solenoid to hook
                cmd_mv = 0x00
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,SOLENOID_OFF],extended_id=False)
                bus.send(msg)
                time.sleep(3)
                #check if hooking is effective
                #Check done by measuring the distance between the two cars
                cmd_mv = 0xBB 
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
                bus.send(msg)
                time.sleep(2)
                measured_distance = int.from_bytes(msg.data[4:6], byteorder='big')
                if measured_distance >  HOOKING_DIST + 2 :
                    print("hooking not effective! ")
                    print("Attempting to rehook!")
                    #drive_forward()
                    time.sleep(3)
                    stop()
                    time.sleep(3)
                    drive_backwards()
                else :
                    print("hooking effective!")
                    
            elif measured_distance <= HOOKING_DIST and magnet_detected == 0 :
                print('Alighment error! \n')
                rehook()
            elif measured_distance > HOOKING_DIST and magnet_detected :
                print('Distance Measurement Error! \n')      
            else:
                print('Backing in progress')
                cmd_mv = 0xAB
                cmd_turn = 0xB0
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
                bus.send(msg)

        elif msg.arbitration_id == HALL:
            magnet_detected =  int.from_bytes(msg.data[0:1], byteorder='big')
            print('Magnet status : ', magnet_detected)
            if magnet_detected :
                print('magnet_detected')
                cmd_mv = 0x00
                cmd_turn =  0xB0
                msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,SOLENOID_OFF,0,0,0,0],extended_id=False)
                bus.send(msg)
                time.sleep(0.5)
                print("exiting loop")
                break 

#tow vehicle after hooking
def tow() :   
    flag_us = False
    cpt_us = 0
    flag_cm = False
    cpt_cm = 0
    flag_ufc = False
    cpt_ufc = 0
    ufc = -1
    cpt_both = 0
    
    print('Towing') 
    cmd_mv = 0xAB
    cmd_turn = 0xB0
    msg = can.Message(arbitration_id=MCM,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
    bus.send(msg)
    go =False
    while True :
        msg = bus.recv()
        if msg.arbitration_id == US1:

            fr_left_distance = int.from_bytes(msg.data[0:2], byteorder='big')
            fr_right_distance = int.from_bytes(msg.data[2:4], byteorder='big')
            ##check obstacles
            if fr_left_distance <= SAFE_FRONT_DIST or fr_right_distance < SAFE_FRONT_DIST :
                print('Stopping')
                cmd_mv = 0x00
                cmd_turn = 0xB0
                #stop towing
                stop()
        else:
            print('Towing Forward!')
            cmd_mv = 0xAB
            cmd_turn = 0xB0
            msg = can.Message(arbitration_id=MCM,data=[cmd_mv, cmd_mv, cmd_turn,0,0,0,0,0],extended_id=False)
            bus.send(msg)

        #retreive second vehicle front US
        if not q.empty():
            if q.qsize() > 1:
                us2=q.get()
                num=q.get()
                if "UFC" in us2:
                    ufc=us2.strip("UFC:")
               #     print(ufc.replace(';',''))
                    ufc=ufc.replace(';','')
                    ufc=int(ufc)
              #      print("ufc:",ufc)
             #   print("us2:",us2)
            else:
                num=q.get()
            #print(num)
            
#        else:
#            print('non')
        trame=False
        msg = bus.recv()
        
        if msg.arbitration_id == US1:
            trame = True
# ultrason arriere centre
            distance = int.from_bytes(msg.data[4:6], byteorder='big')
            message = "URC:" + str(distance)+ ";"
            print(message)
            if distance > LIMIT_DIST:
                cpt_us += 1
                if cpt_us > 2:
                    flag_us = True
                    print('ERROR URC\n',time.strftime("%X"))                   #print('US: décrochage détecté\n')
                    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
                    bus.send(msg)
            elif distance <= LIMIT_DIST:
                cpt_us = 0
#                print('OK\n')
        elif msg.arbitration_id == Hall:
            trame = True
            magnet=int.from_bytes(msg.data[0:1],byteorder='big')
            print(magnet)
            if magnet==0:
                cpt_cm += 1
                if cpt_cm > 2:
                    flag_cm = True
                    print('ERROR CM\n',time.strftime("%X"))
                    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
                    bus.send(msg)
            elif magnet==1:
                cpt_cm = 0
#                print("attache")
        if ufc >LIMIT_DIST:
            cpt_ufc +=1
            if cpt_ufc > 2:
                flag_ufc = True
        else:
            cpt_ufc = 0
        if num==0:
            print('Lost connexion with remote car: décrochage détecté\n')
            msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
            bus.send(msg)
#        print ('ufc:',ufc)

        if trame:
            if flag_cm or flag_us:
                cpt_both += 1
                if cpt_both > 3:
                    if flag_cm:
                        if flag_us and flag_ufc:
                            print("CM && US && UFC")
                            print ('Décrochage: barre perdue')
                            print ('Stopping!')
                            stop()                             
                            time.sleep(3)
                            print ('attempting to rehook ')
                            rehook()
                        elif flag_us or flag_ufc:
                            print("CM && (US || UFC)")
                            print ('Décrochage: us défaillant(s)')
                            stop()
                        else:
                            print("CM")
                            print('Capteur magnétique défaillant')
                            stop()
                    elif flag_us:
                        if flag_ufc:
                            print('US && UFC')
                            print('Décrochage: Capteur magnétique défaillant ou barre cassée')
                            print ('Stopping!')
                            stop()
                        else:
                            print('US')
                            print('US défaillant(s) -> pas de correction possible')
                            print ('Stopping!')
                            stop()
                    exit()

#stops the vehicle
def stop():
    print('Stopping Vehicle')        
    cmd_mv = 0xB0
    cmd_turn = 0xB1
    cmd_pos = 0xB1
    msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
    bus.send(msg)
    time.sleep(1)
    msg = can.Message(arbitration_id=FROM_PI,data=[cmd_mv, cmd_mv, cmd_turn,cmd_pos,0,0,0,0],extended_id=False)
    bus.send(msg)
    print('Vehicle Stopped')

#rehook in case of unhooking
def rehook():
    drive_forward()
    time.sleep(3)
    stop()
    drive_backwards()
    hook()

#print message on terminal
#send error report
#send mail
#def detect(error_flag) :
#to implement

#test 
drive_forward()
stop()
stop()




'''
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    exit()

threads = []
msg = can.Message(arbitration_id=0x010,data=[0xBC, 0xBC, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
bus.send(msg)

try:
    q = queue.Queue()
    connected = -1
    t = Thread(target=listen_can,args=(connected,q),daemon=True)
    threads.append(t)
    t.start()
    t = Thread(target=listen_remote_can,args=(connected,2,q),daemon=True)
    threads.append(t)
    t.start()
    
    #m = Thread(target=main)
    #threads.append(m)
    #m.start()
    
    #f = Thread(target=fault_monitor)
    #threads.append(m)
    #m.start()    
except:
    print ("Error launching thread")
    exit()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    msg = can.Message(arbitration_id=0x010,data=[0x00, 0x00, 0xB0, 0x00, 0x00, 0x00, 0x00, 0x00],extended_id=False)
    bus.send(msg)
    exit()
'''

