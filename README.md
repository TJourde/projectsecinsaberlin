# projectsecinsaberlin
Autonomous Tow Car

## Purpose of this project
This project is about creating a program that can make the AutowCar able to tow autonomously.

### Main features
1. Autonomous Towing & Hooking
2. Error detection/Correction
3. GUI & Email

## Presentation of repository
This repository contains the code to run on both cars (AutowCar and Pink car)
There is also the documentation on the technical aspects of the cars in the documentation folder.

# How to run the program
## Requirements
- Place both cars aligned, the AutowCar in front of the Pink car
- Import the code on both cars
- Connect them to the local network (modify the code if necessary "VarBerlin.py")
- Run main_master on the Autowcar
- Run Main_slave ont the Pink car
- Run the GUI on a computer connected to the network

## GUI
1. Connect to the address of the AutowCar
2. Launch the connection to the Pink car
3. Start the hooking
4. Start the towing

### Monitoring
You can stop the operation at anytime.
If an error occurs, one led or more will turn red and an error code will show up. An email will also be sent to the address configurated in the code.
You must exit both the GUI and the program on the AutowCar in order to reset the program. Rerun those to restart the operation.

## Communication

To enable  the communication between we created a python script. One on the towing vehicle that we consider as the server and the towed vehicle  that we consider as client. 
On the server side  we have a python script  handling all communication through one thread. It creates a socket,  opens a TCP port and listens to incoming connections requests. 
On the client side we have three threads. the first thread creates a socket and establishes a TCP connection through the provided TCP port that is open on the remote. The second thread collects appropriate data and the The third thread  receives from the towing vehicle data through the established  connection. 

## Hooking 
Feature description : For the hooking to take place, we place the tow car in front of the broken vehicle at about   X meters distance and instruct it to start the hooking routine.  The tow car then should back up. While backing up the raspberry evaluates the distance from the rear car using the rear central ultrasonic sensor.  When it gets to the hooking distance within 15 cm, it slows down and opens the solenoid and continues to back up. When it gets to the right distance for hooking and detects the presence of the magnetic sensor on the broken vehicles , it should stop and close the solenoid .  
During the hooking errors are also addressed through a different thread

## Towing
Description: The towing process manages the approach, the processing of data received from the second car, the instructions sent to the motor and solenoid and the detection of errors during towing. 

## Errors detection
Detects errors during towing and hooking

## Errors correction
Corrects the errors if possible





