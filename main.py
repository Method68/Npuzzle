#!/usr/bin/env python
import random, os.path, inquirer, os

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

import sys

from PIL import Image
from resizeimage import resizeimage

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

def file_read(file):
	filegameboard = []
	rfile = file.readlines()
	if len(rfile) == 0:
		print('Error value doesn\'t exist')
		exit()
	numberelem = 0
	for line in rfile:
		numberelem += 1
		line = line.replace('\n', '')
		line = line.replace(' ', '')
		line = line.replace('\t', '')
		if line.isdigit():
			filegameboard.append(int(line))
	if numberelem < 4:
		print('Error incorrect size of board')
		exit()
	test_squareroot_value = numberelem ** 0.5
	decimal = str(test_squareroot_value - int(test_squareroot_value))[1:]
	if decimal != '.0':
		print('Error incorrect size of board')
		exit()
	for i in range(numberelem):
		if i not in filegameboard:
			print('Error value doesn\'t exist')
			exit()
	return filegameboard, int(test_squareroot_value)


def main(argv):
	squareside = 0
	filegameboard = []
	input_board = []
	if argv != None:
		filegameboard, squareside = file_read(open(argv, 'r'))
		input_board = core_solver.set_board(filegameboard, squareside)

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
	
	main_menu_loop = 1
	while main_menu_loop == 1:
		if interface != 1:
			if (input_board == []):
				print("\033[90m")
				squareside = input('\033[92mChoose size for Npuzzle: \n\033[91m')
				#####################
				#Ce check est obligatoire sinon tu peux balance une string ....
				if squareside.isdigit() == False or int(squareside) < 2:
					print("\033[91mBad value select int > 1")
					return
				#####################
				squareside = int(squareside)
				print("\033[90m")
			heuristic, algo = menu_terminal(squareside)
			gamemode = 'ia'
		# Comment this else if you don't want to go in the menu
		# 
		else:
			fenetre = pygame.display.set_mode((640, 480), 0, 32)
			menu_items = ('IA', 'Solo', 'Quit')
			pygame.display.set_caption('Game Menu')
			gm = GameMenu(fenetre, menu_items, input_board)
			# return the choice enter in the menu
			heuristic, algo, squareside, gamemode = gm.run()

		size = squareside*100
		img = Image.open("/home/gabba/Documents/pygame/Npuzzle/photo.jpg").resize((size,size))
		out = open("/home/gabba/Documents/pygame/Npuzzle/photo.jpg", "w")
		img.save(out, "JPEG")

		ia_final_move, allcase = core_solver.call_core(squareside, heuristic, algo, gamemode, input_board)
		if input_board:
			allcase = filegameboard
		if interface == 1:
			main_menu_loop = game.call_game(ia_final_move, squareside, allcase, gamemode, fenetre)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(None)
	elif len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print('\033[91mBad number of argument !')
		exit()
