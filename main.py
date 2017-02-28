#!/usr/bin/env python
import random, os.path, inquirer

#Our stuff
import core_solver
import game
import menu
from menu import GameMenu
import utils
from utils import Block
#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
# if not pygame.image.get_extended():
# 		raise SystemExit("Sorry, extended image module required")

def menu_terminal(squareside):
	####################
	#Select heuristic
	questions = [
		inquirer.List('heuristic',
				message="\033[92mSelect heuristic",
				choices=['\033[91mManhattan', '\033[91mEuclidian', '\033[91mChebyshev'],
			),
		]
	heuristic = inquirer.prompt(questions)
	heuristic = heuristic["heuristic"]
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
	return heuristic, algo


def main():
	squareside = 0
	while 42:
		ginterface = raw_input('\033[92mDo you want a Graphical interface for Npuzzle: \n Default: No\nYes/No:\033[91m')
		if ginterface == "y" or ginterface == "yes":
			ginterface = 1
			break
		if ginterface == "no" or ginterface == "n":
			ginterface = 0
			break
	if ginterface != 1:
		print("\033[90m")
		squareside = int(input('\033[92mChoose size for Npuzzle: \n\033[91m'))
		print("\033[90m")
		heuristic, algo = menu_terminal(squareside)
	# Comment this else if you don't want to go in the menu
	# 
	else:
		screen = pygame.display.set_mode((640, 480), 0, 32)
		menu_items = ('Solo', 'Submenu', 'Quit')
		pygame.display.set_caption('Game Menu')
		gm = GameMenu(screen, menu_items)
		# return the choice enter in the menu
		heuristic, algo, squareside, gamemode = gm.run()

	ia_final_move, allcase = core_solver.call_core(squareside, heuristic, algo)
	if ginterface == 1:
		game.call_game(ia_final_move, squareside, allcase)

if __name__ == '__main__': main()
