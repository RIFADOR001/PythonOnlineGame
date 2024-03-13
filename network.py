import socket

class Network:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server = "192.168.1.235"
		self.port = 5555
		self.addr = (self.server, self.port)
		self.pos = self.connect()

	def getPos(self):
		return self.pos

	def connect(self):
		try:
			self.client.connect(self.addr)
			return self.client.recv(2048).decode()
		except (e):
			print("ERROR: ", e)
			pass

	def send(self, data):
		try:
			self.client.send(str.encode(data))
			return self.client.recv(2048).decode()

		except socket.error as e:
			print("ERROR: ", e)


if __name__ == "__main__":
	n = Network()

	print(n.send("Hello"))
	print(n.send("Working"))
