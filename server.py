import socket
from _thread import *
import sys

server = "192.168.1.235"
# Port that is typically available
port = 5555

# Initializing socket
# That is going to create a connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try: 
	s.bind((server, port))
except socket.error  as e:
	str(e)

# This opens the port
# The argument indicates the amount of people connected
s.listen(2)
print("Waiting for a connection, Server Started")



def threaded_client(conn):
	conn.send(str.encode("Connected"))
	reply = ""
	while True:
		try:
			# We state the amount of bits of information that we expect to get
			data = conn.recv(2048)
			reply = data.decode("utf-8")

			if not data:
				print("Disconnected")
				break
			else:
				print("Recieved: ", reply)
				print("Sending: ", reply)

			conn.sendall(str.encode(reply))

		except (e):
			print("ERROR: ", e)
			break


while True:
	conn, addr = s.accept()
	print("Connected to: ", addr)

	start_new_thread(threaded_client, (conn,))

