import pygame
from network import Network
import pickle
from functools import partial

from icecream import ic

pygame.init()
pygame.font.init()


NOTIFICATION_COLOR = (255, 0, 0)
fontSize = partial(pygame.font.SysFont, "comicsans")

width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
	def __init__(self, text, x, y, color):
		self.text = text
		self.x = x
		self.y = y
		self.color = color
		self.width = 150
		self.height = 100

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
		font = pygame.font.SysFont("comicsans", 40)
		text = font.render(self.text, 1, (255, 255, 255))
		win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

	def click(self, pos):
		x1 = pos[0]
		y1 = pos[1]
		if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
			return True
		else:
			return False


def redrawWindow(win, game, p):
	win.fill((128, 128, 128))
	pygame.display.update()
	# print("redrawWindow")
	if not (game.connected()):
		font = fontSize(60)
		text = font.render("Waiting for Player... ", 1, NOTIFICATION_COLOR, True)
		# win.blit(text, (round(width/2) - round(text.get_width()/2), round(height/2) - round(text.get_height)/2))
		win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
	else:
		font = fontSize(50)
		text = font.render("Your Move", 1, (0, 255, 255))
		win.blit(text, (80, 200))

		text = font.render("Your Oponent", 1, (0, 255, 255))
		win.blit(text, (380, 200))

		move1 = game.get_player_move(0)
		move2 = game.get_player_move(1)
		if game.bothWent():
			text1 = font.render(move1, 1, (0, 0, 0))
			text2 = font.render(move2, 1, (0, 0, 0))
		else:
			if game.p1Went and p == 0:
				text1 = font.render(move1, 1, (0, 0, 0))
			elif game.p1Went:
				text1 = font.render("Locked In", 1, (0, 0, 0))
			else:
				text1 = font.render("Waiting...", 1, (0, 0, 0))
			if game.p2Went and p == 1:
				text2 = font.render(move2, 1, (0, 0, 0))
			elif game.p2Went:
				text2 = font.render("Locked In", 1, (0, 0, 0))
			else:
				text2 = font.render("Waiting...", 1, (0, 0, 0))
		if p == 1:
			win.blit(text2, (100, 350))
			win.blit(text1, (400, 350))
		else:
			win.blit(text1, (100, 350))
			win.blit(text2, (400, 350))

		for btn in btns:
			btn.draw(win)

	pygame.display.update()


btns = [Button("Rock", 50, 500, (255, 0, 0)), Button("Paper", 250, 500, (0, 255, 0)), Button("Scissors", 450, 500, (0, 0, 255))]
def main():
	run = True
	clock = pygame.time.Clock()
	n = Network()
	player = int(n.getP())
	print("You are player ", player)
	ic(player)
	while run:
		clock.tick(60)
		try:
			game = n.send("get")
		except:
			run = False
			print("Couldn't get game")
			break
		# ic(game.bothWent())
		if game.bothWent():
			redrawWindow(win, game, player)
			pygame.time.delay(500)
			try:
				game = n.send("reset")
			except:
				run = False
				print("Couldn't get game")
				break
			font = pygame.font.SysFont("comicsans", 90)
			if (game.winner() == player):
				text = font.render("You Won!", 1, NOTIFICATION_COLOR)
			elif game.winner() == -1:
				text = font.render("Tie Game!", 1, NOTIFICATION_COLOR)
			else:
				text = font.render("You Lost...", 1, NOTIFICATION_COLOR)

			# win.blit(text, (round(width/2) - round(text.get_width()/2), round(height/2) - round(text.get_height()/2)))
			win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
			pygame.display.update()
			pygame.time.delay(2000)
		# print("before for")
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				for btn in btns:
					if btn.click(pos) and game.connected():
						if player == 0:
							if not game.p1Went:
								n.send(btn.text)
						else:
							if not game.p2Went:
								n.send(btn.text)
		redrawWindow(win, game, player)

def menu_screen():
	run = True
	clock = pygame.time.Clock()

	while run:
		clock.tick(60)
		win.fill((128, 128, 128))
		font = fontSize(40)
		text = font.render("Click to continue!", 1, (255, 0, 0))
		win.blit(text, (100, 200))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				run = False

	main()


if __name__ == "__main__":
	while True:
		menu_screen()











