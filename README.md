# projectsecinsaberlin

## Communication

To enable  the communication between we created a python scripts. One on the towing vehicle that we consider as the server and the towed vehicle  that we consider as client. 
On the server side  we have a python script  handling all communication through one thread. It creates a socket,  opens a TCP port and listens to incoming connections requests. 
On the client side we have three threads. the first thread creates a socket and establishes a TCP connection through the provided TCP port that is open on the remote. The second thread collects appropriate data and the The third thread  receives from the towing vehicle data through the established  connection. 

# Hooking 
Feature description : For the hooking to take place, we place the tow car in front of the broken vehicle at about   X meters distance and instruct it to start the hooking routine.  The tow car then should back up. While backing up the raspberry evaluates the distance from the rear car using the rear central ultrasonic sensor.  When it gets to the hooking distance within 15 cm, it slows down and opens the solenoid and continues to back up. When it gets to the right distance for hooking and detects the presence of the magnetic sensor on the broken vehicles , it should stop and close the solenoid .  
During the hooking errors are also addressed through a different thread

# Towing


# Errors detection

# Error correction


