#!/usr/bin/env python
import random, os.path

#Our stuff
import core_solver
import utils
from utils import Block
import inquirer
#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
# if not pygame.image.get_extended():
# 		raise SystemExit("Sorry, extended image module required")

def call_core(squareside, fenetre, answers, algo):
	solvable = None	
	while (solvable == None):
		allvalue = squareside * squareside
		allcase_order = [x for x in range(0, allvalue)]
		allcase_order.pop(0)
		allcase_order.append(0)
		allcase = random.sample(range(allvalue),allvalue)
		finalboard = utils.set_board(allcase_order, squareside)
		gameboard = utils.set_board(allcase, squareside)

		solvable = core_solver.construct(squareside, gameboard, finalboard, answers, algo)
		if (solvable != None):
			print ("\033[92mBoard Builded\033[0m")
			break
		else:
			print ("\033[91mBoard Not Builded\033[0m")
	blocks = []
	blocks = utils.build_board(allcase, squareside, blocks, fenetre)
	return blocks, solvable

def first_draw(squareside, fenetre, blocks):
	i = 0
	while (i < (squareside*squareside)):
		# block-body
		utils.draw_block(blocks, fenetre, i)
		fenetre.blit(blocks[i].body, (blocks[i].x, blocks[i].y))
		pygame.display.update()
		i += 1

def main():
	loop = 1
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	squareside = input('\033[92mChoose size for Npuzzle: \n\033[91m')
	print("\033[90m")
	squareside = int(squareside)

	####################
	#Select heuristic
	questions = [
  		inquirer.List('heuristic',
                message="\033[92mSelect heuristic",
                choices=['\033[91mManhattan', '\033[91mEuclidian', '\033[91mChebyshev'],
            ),
		]
	answers = inquirer.prompt(questions)
	answers = answers["heuristic"]
	#####################

	#####################
	#Select algo if squareside <= 3
	algo = ''
	if squareside <= 3:
		questions = [
  		inquirer.List('algo',
                message="\033[92mSelect algorithm",
                choices=['\033[91mAstar', '\033[91mIDAstar'],
            ),
		]
		algo = inquirer.prompt(questions)
		algo = algo["algo"]
	#####################

	width = squareside

	# First loop which call core_solver.construct to do the job
	blocks, ia_final_move = call_core(squareside,fenetre, answers, algo)

	pygame.init()
	# fond = pygame.image.load("/home/gabba/tmp_trash/puzzle-654962_1920.jpg").convert()
	# fenetre.blit(fond, (0,0))
	pygame.display.flip()
	len_move = len(ia_final_move)
	index_move = 0
	space = 0
	#Display the grid before we start
	first_draw(squareside, fenetre, blocks)

	# Second loop To display player moves
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
				else:
					blocks = utils.key_hook(blocks, event.key, squareside)
		#use space to see the next step
		if space == 1:
			utils.ia_move(ia_final_move, index_move, blocks, squareside)
			# display an background images
			# fenetre.blit(fond, (0,0))
			i = 0
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			fenetre.blit(block0.body, (block0.x, block0.y))
			pygame.display.update()
			# for fenetre font
			# pygame.display.flip()
			index_move += 1
			if index_move == len_move:
				print ("\033[92mWIN")
				break
			space = 0
if __name__ == '__main__': main()
