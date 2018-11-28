#!/usr/bin/env python

import socket

TCP_IP = '10.1.5.224'
TCP_PORT = 9050
BUFFER_SIZE = 20
MESSAGE = bytes('aBcDeF', encoding='utf_8')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	print( "received data:", data)
s.close()
