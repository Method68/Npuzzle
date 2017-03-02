#!/usr/bin/python
 
import pygame
import sys
from pygame.locals import *
pygame.init()

class GameMenu():
	def __init__(self, screen, items, input_board, bg_color=(0,0,0), font=None, font_size=30,
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
		self.input_board = input_board
		if input_board != []:
			self.len_board_custom = len(input_board)
		for index, item in enumerate(items):
			label = self.font.render(item, 1, font_color)

			width = label.get_rect().width
			height = label.get_rect().height

			posx = (self.scr_width / 2) - (width / 2)
			# t_h: total height of text block
			t_h = len(items) * height
			posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

			self.items.append([item, label, (width, height), (posx, posy)])

	squareside = 2
	heursticselected = ''
	algo = ''
	gamechoice = ''
	lastchoice = ''
	backto = ''

	def run(self):
		global squareside
		global heursticselected
		global algo
		global gamechoice
		global lastchoice
		global backto

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
						print (choice_value)
					if event.key == K_UP and choice_value > 0:
						choice_value -= 1
						choice = self.items[choice_value][0]
					elif event.key == K_DOWN and choice_value < (len(self.items) - 1):
						choice_value += 1
						choice = self.items[choice_value][0]
					if event.key == 13:
						validate = 1

			if validate == 1 and choice == 'IA':
				gamechoice = 'ia'
				lastchoice = 'IA'
				backto = 'Menu'
				tmpitem = self.items
				if self.len_board_custom:
					if self.len_board_custom > 2 and self.len_board_custom < 6:
						if self.len_board_custom == 3:
							sub = GameMenu(self.screen, ('3x3', 'Back'), self.input_board)
						elif self.len_board_custom == 4:
							sub = GameMenu(self.screen, ('4x4', 'Back'), self.input_board)
						elif self.len_board_custom == 5:
							sub = GameMenu(self.screen, ('5x5', 'Back'), self.input_board)
				else:
					sub = GameMenu(self.screen, ('2x2', '3x3', '4x4', '5x5', 'Back'), self.input_board)
				sub.run()
				self.items = tmpitem
				mainloop = 0
				break

			elif validate == 1 and choice == 'Solo':
				gamechoice = 'solo'
				lastchoice = 'Solo'
				backto = 'Menu'
				tmpitem = self.items
				if self.len_board_custom:
					if self.len_board_custom > 2 and self.len_board_custom < 6:
						if self.len_board_custom == 3:
							sub = GameMenu(self.screen, ('3x3', 'Back'), self.input_board)
						elif self.len_board_custom == 4:
							sub = GameMenu(self.screen, ('4x4', 'Back'), self.input_board)
						elif self.len_board_custom == 5:
							sub = GameMenu(self.screen, ('5x5', 'Back'), self.input_board)
				else:
					sub = GameMenu(self.screen, ('2x2', '3x3', '4x4', '5x5', 'Back'), self.input_board)
				sub.run()
				self.items = tmpitem
				mainloop = 0
				break

			elif validate == 1 and (choice == '2x2' or choice == '3x3' or choice == '4x4' or choice == '5x5' or (choice == 'Back' and backto == 'Menu')):
				if choice == 'Back':
					choice = 'Menu'
				elif gamechoice == 'ia':
					backto = 'IA'
					if choice == '2x2':
						squareside = 2
					elif choice == '3x3':
						squareside = 3
					elif choice == '4x4':
						squareside = 4
					elif choice == '5x5':
						squareside = 5
					tmpitem = self.items
					sub = GameMenu(self.screen, ('Manhattan Distance', 'Euclidian Distance', 'Chebyshev Distance', 'Back'), self.input_board)
					sub.run()
					self.items = tmpitem
					mainloop = 0
					break
				else:
					heursticselected = ''
					algo = ''
					if choice == '2x2':
						squareside = 2
						return heursticselected, algo, squareside
					elif choice == '3x3':
						squareside = 3
						return heursticselected, algo, squareside
					elif choice == '4x4':
						squareside = 4
						return heursticselected, algo, squareside
					elif choice == '5x5':
						squareside = 5
						return heursticselected, algo, squareside

			elif validate == 1 and (choice == 'Manhattan Distance' or choice == 'Euclidian Distance' or choice == 'Chebyshev Distance' or (choice == 'Back' and backto == 'IA')):
				if choice == 'Back':
					choice = 'IA'
				elif squareside < 4:
					backto = 'Manhattan Distance'
					if choice == 'Manhattan Distance':
						heursticselected = 'Manhattan'
					elif choice == 'Euclidian Distance':
						heursticselected = 'Euclidian'
					elif choice == 'Chebyshev Distance':
						heursticselected = 'Chebyshev'
					tmpitem = self.items
					sub = GameMenu(self.screen, ('Astar', 'IDAstar', 'Back'), self.input_board)
					sub.run()
					self.items = tmpitem
					mainloop = 0
					break
				else:
					if choice == 'Manhattan Distance':
						heursticselected = 'Manhattan'
						algo = 'IDAstar'
						return heursticselected, algo, squareside
					elif choice == 'Euclidian Distance':
						heursticselected = 'Euclidian'
						algo = 'IDAstar'
						return heursticselected, algo, squareside
					elif choice == 'Chebyshev Distance':
						heursticselected = 'Chebyshev'
						algo = 'IDAstar'
						return heursticselected, algo, squareside

			elif validate == 1 and (choice == 'Astar' or choice == 'IDAstar' or (choice == 'Back' and backto == 'Manhattan Distance')):
				if choice == 'Back':
					choice = '2x2'
				else:
					if choice == 'Astar':
						algo = 'Astar'
						return heursticselected, algo, squareside
					elif choice == 'IDAstar':
						algo = 'IDAstar'
						return heursticselected, algo, squareside

			elif validate == 1 and choice == 'Menu':
				tmpitem = self.items
				sub = GameMenu(self.screen, ('IA', 'Solo', 'Quit'), self.input_board)
				sub.run()
				self.items = tmpitem
				mainloop = 0
				break

			elif validate == 1 and choice == 'Return':
				return 'Manhattan', 'IDAstar', 2

			elif validate == 1 and choice == 'Quit':
				sys.exit()

			# Redraw the background
			self.screen.fill(self.bg_color)
			for name, label, (width, height), (posx, posy) in self.items:
				self.screen.blit(label, (posx, posy))
				if name == choice:
					self.screen.blit(self.font.render(('X'), 1, (255,0,0)), (200, posy))
			pygame.display.flip()

		#get the rigth value
		return heursticselected, algo, squareside, gamechoice