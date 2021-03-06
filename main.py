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
if not pygame.image.get_extended():
		raise SystemExit("Sorry, extended image module required")

def terminal_menu(squareside):
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
	linePos = 0
	filegameboard = []
	rfile = file.readlines()
	if len(rfile) == 0:
		print('\033[91mError value doesn\'t exist\033[0m')
		exit()
	numberelem = 0
	numberCol = 0
	squareside = 0
	for line in rfile:
		numberRaw = 0
		line = line.replace('\t', ' ')
		line = line.replace(' ', ',')
		if ('#' in line):
			line = line.split('#', 1)[0]
		if (line == ''):
			continue
		if (line == ''):
			print('\033[91mError empty line\033[0m')
			exit()
		if (line != '\n'):
			line = line.replace('\n', '')
		if linePos == 0:
			if not line.isdigit():
				print('\033[91mError incorrect value\033[0m')
				exit()
			else:
				squareside = int (line)
		else:
			if (line == ''):
				print('\033[91mError empty line\033[0m')
				exit()
			if (line != '\n'):
				line = line.replace('\n', '')
			line = line.replace('\t', ' ')
			lineElem = line.split(',')
			for elem in lineElem:
				if elem.isdigit():
					numberelem += 1
					numberRaw += 1
					filegameboard.append(int(elem))
				elif (elem == '#'):
					break
				elif (elem == ''):
					break
				else:
					print('\033[91mError incorrect size of board\033[0m')
					exit()

		if (linePos != 0 and numberRaw != squareside):
			print('\033[91mError incorrect size of board\033[0m')
			exit()
		numberCol += 1
		linePos += 1

	if (numberCol -1!= squareside):
		print('\033[91mError incorrect size of board\033[0m'+str(numberCol))
		exit()

	# test_squareroot_value = numberelem ** 0.5
	# decimal = str(test_squareroot_value - int(test_squareroot_value))[1:]
	# if decimal != '.0':
	# 	print('\033[91m 4Error incorrect size of board\033[0m')
	# 	exit()
	for i in range(numberelem):
		if i not in filegameboard:
			print('\033[91mError value out of range\033[0m')
			exit()
	return filegameboard, int(squareside)

def graphical_interface_mode():
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
	return interface

def game_setting_menu(interface, input_board, squareside):
	fenetre = None
	if interface != 1:
		if (input_board == []):
			print("\033[90m")
			squareside = input('\033[92mChoose size for Npuzzle: \n\033[91m')
			#####################
			#Ce check est obligatoire sinon tu peux balance une string ....
			if squareside.isdigit() == False or int(squareside) < 2:
				print("\033[91mBad value select int > 1\033[0m")
				exit()
			elif int(squareside) > 100:
				print("\033[91mDo you really wanna wait forever ??\033[0m")
				exit()
			#####################
			squareside = int(squareside)
			print("\033[90m")
		heuristic, algo = terminal_menu(squareside)
		gamemode = 'ia'
		# Comment this else if you don't want to go in the menu
		# 
	else:
		fenetre = pygame.display.set_mode((1000, 800), 0, 32)
		menu_items = ('IA', 'Solo', 'Quit')
		pygame.display.set_caption('Game Menu')
		gm = GameMenu(fenetre, menu_items, input_board)
		# return the choice enter in the menu
		heuristic, algo, squareside, gamemode = gm.run()
	return heuristic, algo, squareside, gamemode, fenetre

def main(argv):
	squareside = 0
	filegameboard = []
	input_board = []
	fenetre = None
	file_from_input = 0
	if argv != None:
		try:
			fd = open(argv, 'r')
		except FileNotFoundError:
			print("\033[91mFile doesn't exist\033[0m")
			exit()
		filegameboard, squareside = file_read(open(argv, 'r'))
		input_board = core_solver.set_board(filegameboard, squareside)
		file_from_input = 1
	interface = graphical_interface_mode()
	try:
		Image.open("/Users/gkuma/Downloads/photo_200_.jpg")
	except IOError:
		game_size = 2
		while (game_size < 6):
			size = game_size*100
			try:
				img = Image.open("/Users/gkuma/Downloads/photo.jpg").resize((size,size))
			except FileNotFoundError:
				print("\033[91mImage doesn't exist, Please drop an image named 'photo.jpg' there:\nPath:/Users/gkuma/Downloads/photo.jpg \033[0m")
				exit()
			out = open("/Users/gkuma/Downloads/photo_"+str(size)+"_"+".jpg", "w")
			img.save(out, "JPEG")
			game_size += 1
	main_menu_loop = 1
	while main_menu_loop == 1:
		heuristic, algo, squareside, gamemode, fenetre = game_setting_menu(interface, input_board, squareside)
		ia_final_move, allcase = core_solver.call_core(squareside, heuristic, algo, gamemode, input_board)
		if input_board:
			allcase = filegameboard
		if interface == 1:
			main_menu_loop = game.call_game(ia_final_move, squareside, allcase, gamemode, fenetre)
		if file_from_input:
			filegameboard, squareside = file_read(open(argv, 'r'))
			input_board = core_solver.set_board(filegameboard, squareside)
		ia_final_move = []
		allcase = []


if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(None)
	elif len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print('\033[91mBad number of argument !')
		exit()
