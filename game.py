import pygame
from pygame.locals import *
import utils
from utils import Block
import menu
from menu import GameMenu
import replay
from replay import ReplayMenu
import image_slicer
from core_solver import set_finalboard ,set_board
import time

def display_nbr_move(fenetre, total_move):
	# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
	myfont = pygame.font.SysFont("monospace", 15)

	# render text
	label = myfont.render("Move Total", 1, (255,255,0))
	label2 = myfont.render(str(total_move), 1, (255,255,0))
	fenetre.blit(label, (600, 100))
	fenetre.blit(label2, (600, 120))

def display_ia_mode(fenetre, auto):
	myfont = pygame.font.SysFont("monospace", 15)
	titre_key = myfont.render("Press space: step by step", 1, (255,255,0))
	titre_auto = myfont.render("Press enter: Auto mode", 1, (255,255,0))
	label = myfont.render("Mode auto:", 1, (255,255,0))
	if (auto == 0):
		label2 = myfont.render("off", 1, (255,0,0))
	if (auto == 1):
		label2 = myfont.render("on", 1, (0,255,0))
	fenetre.blit(titre_key, (200, 100))
	fenetre.blit(titre_auto, (200, 120))
	fenetre.blit(label, (200, 140))
	fenetre.blit(label2, (350, 140))

def display_timer(fenetre, timer, milliseconds, seconds, minutes):
	if milliseconds > 1000:
		seconds += 1
		milliseconds -= 1000
	if seconds > 60:
		minutes += 1
		seconds -= 60
	myfont = pygame.font.SysFont("monospace", 15)
	t_txt = myfont.render("time : ", 1, (255,255,0))
	timer_txt = myfont.render(str(minutes)+":"+str(seconds)+":"+str(milliseconds), 1, (255,255,0))
	pygame.draw.rect(fenetre, [45, 50, 70], (350, 100, 200, 15))
	fenetre.blit(t_txt, (350, 100))
	fenetre.blit(timer_txt, (400, 100))
	pygame.display.flip()
	return milliseconds, seconds, minutes

def main_loop_solo(squareside, fenetre, blocks, fond):
	index_move = 0
	loop = 1
	space = 0
	total_move = 1
	ia_final_move = 0
	movelen = 0
	move = []
	gameboard = []
	for elem in blocks:
		gameboard.append(int(elem.number))
	gameboard = set_board(gameboard, squareside)
	print ("gameboard")
	print (gameboard)
	final_board = set_finalboard(squareside)
	timer = pygame.time.Clock()
	minutes = 0
	seconds = 0
	milliseconds = 0
	while loop:
		milliseconds += timer.tick_busy_loop(60)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				move = []
				print ("\n\nDEBUG")
				print (event.key)
				print (move)
				print ("\n\n")
				if event.key == 273:
					move.append('UP')
					movelen = 1
				elif event.key == 274:
					move.append('DOWN')
					movelen = 1
				elif event.key == 276:
					move.append('LEFT')
					movelen = 1
				elif event.key == 275:
					move.append('RIGHT')
					movelen = 1
				elif event.key == K_ESCAPE:
					loop = 0 
					movelen = 1
			elif event.type == QUIT:
				loop = 0

		if movelen == 1 and len(move) == 1:
			blocks, gameboard = utils.player_move(move, 0, blocks, squareside, gameboard)
			case = None

			for i in range(squareside):
				try:
					case = gameboard[i].index(0)
				except Exception as e:
					continue
				case = (i, case)
				break
			if move[0] == 'UP' and case[0] > 0:
				gameboard[case[0]][case[1]], gameboard[case[0]-1][case[1]] = gameboard[case[0]-1][case[1]], gameboard[case[0]][case[1]]
			elif move[0] == 'DOWN' and case[0] < (squareside - 1):
				gameboard[case[0]][case[1]], gameboard[case[0]+1][case[1]] = gameboard[case[0]+1][case[1]], gameboard[case[0]][case[1]]
			elif move[0] == 'LEFT' and case[1] > 0:
				gameboard[case[0]][case[1]-1], gameboard[case[0]][case[1]] = gameboard[case[0]][case[1]], gameboard[case[0]][case[1]-1]
			elif move[0] == 'RIGHT' and case[1] < (squareside - 1):
				gameboard[case[0]][case[1]+1], gameboard[case[0]][case[1]] = gameboard[case[0]][case[1]], gameboard[case[0]][case[1]+1]
			i = 0
			fenetre.blit(fond, (0,0))
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			pygame.draw.rect(fenetre, [238, 0, 0], (block0.x, block0.y, 100, 100), 1)
			display_nbr_move(fenetre, total_move)
			pygame.display.flip()
			lenmove = 0
			move = []
			total_move += 1
			print ("block")
			print (gameboard)
			if (gameboard == final_board):
				print ("\033[92mWIN\033[0m")
				break
		move = []
		milliseconds, seconds, minutes = display_timer(fenetre, timer, milliseconds, seconds, minutes)
	print ("Final score \n time {}:{}:{}\n total_move {}".format(minutes, seconds, milliseconds, total_move))

def main_loop(ia_final_move, squareside, fenetre, blocks, fond):
	len_move = len(ia_final_move)
	index_move = 0
	total_move = 1
	loop = 1
	space = 0
	auto = 0
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
				elif event.key == K_ESCAPE:
					loop = 0
				elif event.key == 13:
					if (auto == 1):
						auto = 0
					else:
						auto = 1
					space = 1
		if space == 1 and len_move > 0:
			utils.ia_move(ia_final_move, index_move, blocks, squareside)
			fenetre.blit(fond, (0,0))
			i = 0
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			fenetre.blit(block0.background, (block0.x, block0.y))
			pygame.draw.rect(fenetre, [238, 0, 0], (block0.x, block0.y, 100, 100), 1)
			display_nbr_move(fenetre, total_move)
			display_ia_mode(fenetre, auto)
			pygame.display.flip()
			index_move += 1
			if index_move == len_move:
				print ("\033[92mWIN\033[0m")
				break
			if auto == 1:
				space = 1
				pygame.time.wait(100)
			else:
				space = 0
			total_move += 1

def first_draw(squareside, fenetre, blocks, gamemode):
	i = 0
	total_move = 0
	while (i < (squareside*squareside)):
		utils.draw_block(blocks, fenetre, i)
		fenetre.blit(blocks[i].background, (blocks[i].x, blocks[i].y))
		pygame.draw.rect(fenetre, [238, 238, 224], (blocks[i].x, blocks[i].y, 100, 100), 1)
		block0 = utils.get_block_zero(blocks)
		fenetre.blit(block0.background, (block0.x, block0.y))
		pygame.draw.rect(fenetre, [238, 0, 0], (block0.x, block0.y, 100, 100), 1)
		pygame.display.update()
		i += 1
	if (gamemode == 'ia'):
		display_ia_mode(fenetre, 0)
		display_nbr_move(fenetre, total_move)	
	elif (gamemode == 'solo'):
		display_nbr_move(fenetre, total_move)

def call_game(ia_final_move, squareside, allcase, gamemode, fenetre):
	tiles = image_slicer.slice("/Users/gkuma/Downloads/photo_"+str(squareside*100)+"_.jpg", squareside*squareside, save=False)
	image_slicer.save_tiles(tiles, directory='/Users/gkuma/Downloads/', prefix='')
	replay = 1
	while (replay == 1):
		blocks = []
		blocks = utils.build_board(allcase, squareside, blocks, fenetre)
		fond = pygame.image.load("/Users/gkuma/Downloads/background.jpg")
		fenetre.blit(fond, (0,0))
		first_draw(squareside, fenetre, blocks, gamemode)
		pygame.display.flip()	
		if gamemode == 'ia':
			main_loop(ia_final_move, squareside, fenetre, blocks, fond)
		if gamemode == 'solo':
			main_loop_solo(squareside, fenetre, blocks, fond)
		pygame.time.wait(3000)
		menu_items = ('Replay', 'MainMenu', 'Quit')
		pygame.display.set_caption('Replay')
		replay_menu = ReplayMenu(fenetre, menu_items)
		# return the choice enter in the menu
		replay = replay_menu.run()
	if replay == 2:
		replay = 1
	return replay