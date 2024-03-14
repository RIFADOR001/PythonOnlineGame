import pygame

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