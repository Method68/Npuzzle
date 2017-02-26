#!/usr/bin/env python
import random, os.path

#Our stuff
import core_solver
import utils

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
		raise SystemExit("Sorry, extended image module required")

class Rect(object):
	"""__init__() functions as the class constructor"""
	def __init__(self, fenetre=None, x=None, y=None, i=None):
		print ("obj"+str(i))
		if i == 0:
			print ("i = 0")
			self.color = (180, 205, 205)
		else :
			# self.color = (((i * 3)+150, (i * 4)+150, (i * 1)+150))
			self.color = (255, 255, 255)
		self.x = x
		self.y = y
		self.body = pygame.Surface((utils.blocksize,utils.blocksize))
		self.body.fill(self.color)
		self.number = str(i)
		# print ("My number is")
		# print (self.number)

def create_a_solvable_grid(width, squareside, allcase, allcase_order):
	finalboard = utils.set_board(allcase_order, width)
	gameboard = utils.set_board(allcase, width)

	solvable = core_solver.construct(squareside, gameboard, finalboard)
	if (solvable != None):
		print ("Board Builded")
		return solvable
	else:
		print ("Board Not Builded")
		return None

def first_draw(squareside, fenetre, rects):
	i = 0
	while (i < (squareside*squareside)):
		# block-body
		utils.draw_block(rects, fenetre, i)
		fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
		pygame.display.update()
		i += 1

def main():
	loop = 1
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	squareside = input('\033[92mChoose size for Npuzzle: \n')
	squareside = int(squareside)
	width = squareside
	solvable = None
	
	# First loop which call core_solver.construct to do the job
	while (solvable == None):
		allvalue = width * width
		allcase_order = [x for x in range(0, allvalue)]
		allcase_order.pop(0)
		allcase_order.append(0)
		allcase = random.sample(range(allvalue),allvalue)
		ia_final_move = create_a_solvable_grid(width, squareside, allcase, allcase_order)
		if ia_final_move:
			solvable = ia_final_move
		rects = []
		rects = utils.build_board(allcase, squareside, rects, fenetre)

	pygame.init()
	# fond = pygame.image.load("/home/gabba/tmp_trash/puzzle-654962_1920.jpg").convert()
	# fenetre.blit(fond, (0,0))
	pygame.display.flip()
	len_move = len(ia_final_move)
	index_move = 0
	space = 0
	#Display the grid before we start
	first_draw(squareside, fenetre, rects)

	# Second loop To display player moves
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
				else:
					rects = utils.key_hook(rects, event.key, squareside)
		#use space to see the next step
		if space == 1:
			utils.ia_move(ia_final_move, index_move, rects, squareside)
			# display an background images
			# fenetre.blit(fond, (0,0))
			i = 0
			while (i < (squareside*squareside)):
				utils.draw_block(rects, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(rects)
			fenetre.blit(block0.body, (block0.x, block0.y))
			pygame.display.update()
			# for fenetre font
			# pygame.display.flip()
			index_move += 1
			if index_move == len_move:
				print ("WIN")
				break
			space = 0
if __name__ == '__main__': main()
