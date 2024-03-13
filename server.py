import socket
from _thread import *
import sys

server = "192.168.1.235"
# Port that is typically available
port = 5555

# Initializing socket
# That is going to create a connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def read_pos(s):
	s = s.split(",")
	return int(s[0]), int(s[1])

def make_pos(tup):
	return str(tup[0]) + "," + str(tup[1])

try: 
	s.bind((server, port))
except socket.error  as e:
	str(e)

# This opens the port
# The argument indicates the amount of people connected
s.listen(2)
print("Waiting for a connection, Server Started")


pos = [(0, 0), (100, 100)]
def threaded_client(conn, player):
	conn.send(str.encode(make_pos(pos[player])))
	reply = ""
	while True:
		try:
			# We state the amount of bits of information that we expect to get
			rec = conn.recv(2048).decode()
			# We verify if we still get recieve information
			if not rec:
				print("Player disconnected")
				break
			data = read_pos(rec)
			pos[player] = data

			if not data:
				print("Disconnected")
				break
			else:
				if player == 1:
					reply = pos[0]
				else:
					reply = pos[1]
				print("Recieved: ", data)
				print("Sending: ", reply)

			conn.sendall(str.encode(make_pos(reply)))

		except socket.error as e:
			print("ERROR: ", e)
			break

currentPlayer = 0
while True:
	conn, addr = s.accept()
	print("Connected to: ", addr)

	start_new_thread(threaded_client, (conn, currentPlayer))
	currentPlayer += 1






