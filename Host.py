# setup host
import socket
import sys
import time

# Configurable Parameters
HOST = "localhost"
PORT = 14551

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)					# Allow socket to be reused
print("Socket created")

# bind socket to port
try:
	s.bind((HOST,PORT))
except socket.error as msg:
	print("Error binding")
	#print("Error Bind: {} Message {}".format(str(msg[0], msg[1]))
	

print("Socket bind Success")

# Begin listening for for 5 clients
s.listen(5)
print("Listening...")

while 1:
	# wait and accept client connections
	conn, addr = s.accept()
	print("Client connected ({}, {})".format(addr[0], addr[1]))
	data = b'$GPGGA,165103.833,3459.05955,N,11751.82218,W,1,11,0.98,701.13,M,0,M,,*68\n$GPGLL,3459.06,N,11751.82,W,165103.833,A,A*47\n$GPHDG,11.3,0,E,0,E*6D\n$GPVTG,150,011,00.2,00.3*57\n$GPRMC,165103.834,A,3459.05955,N,11751.82218,W,0.2,150.2,030220,0,E,A*04\n$GPRPY,1.46283,2.17780,11.25614,*57\n$GPGGA,165107.835,3459.05964,N,11751.82214,W,1,12,0.91,701.12,M,0,M,,*6F\n$GPGLL,3459.06,N,11751.82,W,165107.835,A,A*45\n$GPHDG,11.3,0,E,0,E*6D\n$GPVTG,150,011,00.2,00.3*57\n$GPRMC,165107.835,A,3459.05964,N,11751.82214,W,0.2,150.2,030220,0,E,A*0F\n$GPRPY,1.45344,2.12522,11.26878,*56\n$GPGGA,165111.838,3459.05963,N,11751.82188,W,1,12,0.91,701.13,M,0,M,,*65\n$GPGLL,3459.06,N,11751.82,W,165111.838,A,A*4F\n$GPHDG,11.4,0,E,0,E*6A\n$GPVTG,150,011,00.3,00.5*50\n$GPRMC,165111.839,A,3459.05963,N,11751.82188,W,0.3,150.2,030220,0,E,A*04\n$GPRPY,1.46543,2.11837,11.36905,*54\n$GPGGA,165115.841,3459.05954,N,11751.82155,W,1,12,0.91,701.07,M,0,M,,*6E\n'
	conn.send(data)
	print("Sent to client: {}".format(data))
