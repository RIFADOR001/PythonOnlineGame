import pygame
from network import Network

pygame.init()

width = 500
height = 500

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0


class Player:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y 
		self.width = width
		self.height = height
		self.color = color
		self.rect = (x, y, width, height)
		self.vel = 3

	def updateRectangle(self):
		self.rect = (self.x, self.y, self.width, self.height)

	def draw(self, win):
		pygame.draw.rect(win, self.color, self.rect)

	def move(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_LEFT]:
			self.x -= self.vel
			print("left")

		if keys[pygame.K_RIGHT]:
			self.x += self.vel
			print("right")

		if keys[pygame.K_UP]:
			self.y -= self.vel
			print("up")

		if keys[pygame.K_DOWN]:
			self.y += self.vel
			print("down")
		self.updateRectangle()


def read_pos(s):
	s = s.split(",")
	return int(s[0]), int(s[1])

def make_pos(tup):
	return str(tup[0]) + "," + str(tup[1])

def redrawWindow(win, player, player2):
	win.fill((255,255,255))
	player.draw(win)
	player2.draw(win)
	pygame.display.update()



def main():
	run = True
	n = Network()
	# We get the position from the server
	startPos = read_pos(n.getPos())
	p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
	p2 = Player(0, 0, 100, 100, (0, 0, 255))

	#To define the fps
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)
		# Now we send our position and get the position of the other player
		p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
		p2.x = p2Pos[0]
		p2.y = p2Pos[1]
		p2.updateRectangle()


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("quit")
				run = False
				pygame.quit()
		p.move()
		redrawWindow(win, p, p2)


if __name__ == "__main__":
	main()











