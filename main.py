#!/usr/bin/env python
import random, os.path, inquirer, os

#Our stuff
from  tkinter import *
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
	if heuristic == '\033[91mEuclidian':
		heuristic = "Euclidian"
	elif heuristic == '\033[91mManhattan':
		heuristic = "Manhattan"
	else:
		heuristic = "Chebyshev"
	#####################

	#####################
	#Select algo if squareside <= 3
	algo = 'IDAstar'
	if squareside <= 3:
		questions = [
		inquirer.List('algo',
				message="\033[92mSelect algorithm",
				choices=['\033[91mAstar', '\033[91mIDAstar'],
			),
		]
		algo = inquirer.prompt(questions)
		algo = algo["algo"]
		if algo == '\033[91mAstar':
			algo = 'Astar'
		else:
			algo = 'IDAstar'
	#####################
	return heuristic, algo


def main(argv):
	squareside = 0
	###################
	#for read file
	#filegameboard = ''
	#if argv != None:
	#	filename = argv
	#	def file_read(file):
	#		rfile = file.readlines()
	#		if len(rfile) > 1:
	#			print('\033[91mExemple of valid board on same line : [[1,2,3],[4,5,6],[7,8,0]]')
	#			exit()
	#		else:
	#			filegameboard = rfile
	#	file = file_read(open(filename, 'r'))

	while 42:
		#####################
		#Select interface Yes, No
		questions = [
		inquirer.List('interface',
				message="\033[92mDo you want a Graphical interface for Npuzzle:",
				choices=['\033[91mYes', '\033[91mNo'],
			),
		]
		interface = inquirer.prompt(questions)
		interface = interface["interface"]
		#####################
		if interface == "\033[91mYes":
			interface = 1
			break
		else:
			interface = 0
			break
	if interface != 1:
		print("\033[90m")
		squareside = input('\033[92mChoose size for Npuzzle: \n\033[91m')
		#####################
		#Ce check est obligatoire sinon tu peux balance une string ....
		if squareside.isdigit() == False or int(squareside) < 2:
			return(print('\033[91mBad value select int > 1'))
		#####################
		squareside = int(squareside)
		print("\033[90m")
		heuristic, algo = menu_terminal(squareside)
		gamemode = 'ia'
	# Comment this else if you don't want to go in the menu
	# 
	else:
		screen = pygame.display.set_mode((640, 480), 0, 32)
		menu_items = ('IA', 'Solo', 'Quit')
		pygame.display.set_caption('Game Menu')
		gm = GameMenu(screen, menu_items)
		# return the choice enter in the menu
		heuristic, algo, squareside, gamemode = gm.run()

	ia_final_move, allcase = core_solver.call_core(squareside, heuristic, algo, gamemode)
	if interface == 1:
		game.call_game(ia_final_move, squareside, allcase, gamemode)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(None)
	elif len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print('\033[91mBad number of argument !')
		exit()
