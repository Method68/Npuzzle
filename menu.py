#!/usr/bin/python
 
import pygame
import sys
from pygame.locals import *
pygame.init()

class GameMenu():
	def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
					font_color=(255, 255, 255)):
		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height

		self.bg_color = bg_color
		self.clock = pygame.time.Clock()

		self.items = items
		self.font = pygame.font.SysFont(font, font_size)
		self.font_color = font_color

		self.items = []
		for index, item in enumerate(items):
			label = self.font.render(item, 1, font_color)

			width = label.get_rect().width
			height = label.get_rect().height

			posx = (self.scr_width / 2) - (width / 2)
			# t_h: total height of text block
			t_h = len(items) * height
			posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

			self.items.append([item, label, (width, height), (posx, posy)])
 
	def run(self):
		mainloop = True
		choice = self.items[0][0]
		choice_value = 0
		validate = 0
		posxy = self.items[0][3]
		posx = posxy[0]
		posy = posxy[1]
		self.screen.blit(self.font.render(('X'), 1, (255,0,0)), (posx + 100, posy))
		while mainloop:
			# Limit frame speed to 50 FPS
			self.clock.tick(50)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainloop = False
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						mainloop = False
						print choice_value
					if event.key == K_UP and choice_value > 0:
						choice_value -= 1
						choice = self.items[choice_value][0]
					elif event.key == K_DOWN and choice_value < (len(self.items) - 1):
						choice_value += 1
						choice = self.items[choice_value][0]
					if event.key == 13:
						validate = 1

			if validate == 1 and choice == 'Solo':
				print ("createa new submenue:")
				print (choice)
				break
			elif validate == 1 and choice == 'Submenu':
				sub = GameMenu(self.screen, ('Start2', 'Submenu', 'Quit'))
				heuristic, algo, squareside = sub.run()
			elif validate == 1 and choice == 'Quit':
				sys.exit()

			# Redraw the background
			self.screen.fill(self.bg_color)
			for name, label, (width, height), (posx, posy) in self.items:
				self.screen.blit(label, (posx, posy))
				if name == choice:
					self.screen.blit(self.font.render(('X'), 1, (255,0,0)), (posx + 100, posy))
			pygame.display.flip()

		#get the rigth value
		heuristic = 'Manhattan'
		algo = 'IDAstar'
		squareside = 2
		return heuristic, algo, squareside