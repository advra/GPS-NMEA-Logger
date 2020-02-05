# setup host
import socket
import sys
import time

# Configurable Parameters
HOST = "localhost"
PORT = 14551
WAIT_EACH_SEND = 0.25

datas = [b'$GPGGA,165103.833,3459.05955,N,11751.82218,W,1,11,0.98,701.13,M,0,M,,*68\r\n',
		b'$GPGLL,3459.06,N,11751.82,W,165103.833,A,A*47\r\n',
		b'$GPHDG,11.3,0,E,0,E*6D\r\n',
		b'$GPVTG,150,011,00.2,00.3*57\r\n'
		b'$GPRMC,165103.834,A,3459.05955,N,11751.82218,W,0.2,150.2,030220,0,E,A*04\r\n',
		b'$GPRPY,1.46283,2.17780,11.25614,*57\r\n',
		b'$GPGGA,165107.835,3459.05964,N,11751.82214,W,1,12,0.91,701.12,M,0,M,,*6F\r\n',
		b'$GPGLL,3459.06,N,11751.82,W,165107.835,A,A*45\r\n',
		b'$GPHDG,11.3,0,E,0,E*6D\r\n',
		b'$GPVTG,150,011,00.2,00.3*57\r\n',
		b'$GPRMC,165107.835,A,3459.05964,N,11751.82214,W,0.2,150.2,030220,0,E,A*0F\r\n',
		b'$GPRPY,1.45344,2.12522,11.26878,*56\r\n',
		b'$GPGGA,165111.838,3459.05963,N,11751.82188,W,1,12,0.91,701.13,M,0,M,,*65\r\n',
		b'$GPGLL,3459.06,N,11751.82,W,165111.838,A,A*4F\r\n',
		b'$GPHDG,11.4,0,E,0,E*6A\r\n',
		b'$GPVTG,150,011,00.3,00.5*50\r\n',
		b'$GPRMC,165111.839,A,3459.05963,N,11751.82188,W,0.3,150.2,030220,0,E,A*04\r\n',
		b'$GPRPY,1.46543,2.11837,11.36905,*54\r\n',
		b'$GPGGA,165115.841,3459.05954,N,11751.82155,W,1,12,0.91,701.07,M,0,M,,*6E\r\n'
		]

def setup():
	# Create socket and allow socket to be reused
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)					
	print("Socket created")

	# Bind socket to port
	try:
		s.bind((HOST,PORT))
		print("Socket bind Success")
	except socket.error as msg:
		print("Error Bind: {} Message {}".format(str(msg[0], msg[1])))
		sys.exit()

	# Begin listening for for 5 clients
	s.listen(5)
	print("Listening...")
	
	return s

def run(sock):
	i = 0

	while 1:
		# wait and accept client connections
		conn, addr = sock.accept()
		print("Client connected ({}, {})".format(addr[0], addr[1]))
		
		# client connected begin transmission
		while 1:
			if i >= len(datas):
				i = 0
			conn.send((datas[i]))
			print("Send: {}".format(datas[i]))
			i+=1
			time.sleep(WAIT_EACH_SEND)
		
if __name__ == "__main__":
	sock = setup()
	run(sock)
