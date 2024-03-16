import socket
from _thread import *
from game import Game
import pickle

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
s.listen()
print("Waiting for a connection, Server Started")


connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
	conn.send(str.encode(str(p)))

	reply = ""
	while True:
		try:
			data = conn.recv(4096).decode()

			if gameId in games:
				game = games[gameId]

				if not data:
					break
				else:
					if data == "reset":
						game.resetWent()
						data = None
					elif data != "get":
						game.play(p, data)
					reply = game
					conn.sendall(pickle.dumps(reply))
			else:
				break
		except socket.error as e:
			print("ERROR: ", e)
			break
	print("Lost connection")
	try:
		del games[gameId]
		print("Clossing game ", gameId)
	except:
		pass
	conn.close()


while True:
	conn, addr = s.accept()
	print("Connected to: ", addr)

	idCount += 1
	p = 0
	gameId = (idCount - 1)//2
	if idCount % 2 == 1:
		games[gameId] = Game(gameId)
		print("Creating a new game...")
	else:
		try:
			games[gameId].ready = True
			p = 1
		except:
			pass

	start_new_thread(threaded_client, (conn, p, gameId))








