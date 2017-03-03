import pygame
from pygame.locals import *
import utils
from utils import Block
import menu
from menu import GameMenu
import image_slicer
from core_solver import set_finalboard ,set_board

def main_loop_solo(squareside, fenetre, blocks, fond):
	index_move = 0
	loop = 1
	space = 0
	ia_final_move = 0
	movelen = 0
	move = []
	gameboard = []
	for elem in blocks:
		print (elem.number)
		gameboard.append(int(elem.number))
	gameboard = set_board(gameboard, squareside)
	print ("gameboard")
	print (gameboard)
	final_board = set_finalboard(squareside)
	while loop:
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == 273:
					move.append('UP')
				elif event.key == 274:
					move.append('DOWN')
				elif event.key == 276:
					move.append('LEFT')
				elif event.key == 275:
					move.append('RIGHT')
				elif event.key == K_ESCAPE:
					loop = 0 
				movelen = 1
			elif event.type == QUIT:
				loop = 0
		if movelen == 1 and len(move) > 0:
			blocks, gameboard = utils.player_move(move, 0, blocks, squareside, gameboard)
			case = None

			for i in range(squareside):
				try:
					case = gameboard[i].index(0)
				except Exception as e:
					continue
				case = (i, case)
				break

			if event.key == 273 and case[0] > 0:
				gameboard[case[0]][case[1]], gameboard[case[0]-1][case[1]] = gameboard[case[0]-1][case[1]], gameboard[case[0]][case[1]]
			elif event.key == 274 and case[0] < (squareside - 1):
				gameboard[case[0]][case[1]], gameboard[case[0]+1][case[1]] = gameboard[case[0]+1][case[1]], gameboard[case[0]][case[1]]
			elif event.key == 276 and case[1] > 0:
				gameboard[case[0]][case[1]-1], gameboard[case[0]][case[1]] = gameboard[case[0]][case[1]], gameboard[case[0]][case[1]-1]
			elif event.key == 275 and case[1] < (squareside - 1):
				gameboard[case[0]][case[1]+1], gameboard[case[0]][case[1]] = gameboard[case[0]][case[1]], gameboard[case[0]][case[1]+1]
			
			i = 0
			fenetre.blit(fond, (0,0))
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			# fenetre.blit(block0.background, (block0.x, block0.y))
			pygame.draw.rect(fenetre, [238, 0, 0], (block0.x, block0.y, 100, 100), 1)
			pygame.display.flip()
			lenmove = 0
			move = []
			print ("block")
			print (gameboard)
			if (gameboard == final_board):
				print ("win")
				break

def main_loop(ia_final_move, squareside, fenetre, blocks, fond):
	len_move = len(ia_final_move)
	index_move = 0
	loop = 1
	space = 0
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
				elif event.key == K_ESCAPE:
					loop = 0
		#use space to see the next step
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

			# pygame.display.update()
			pygame.display.flip()
			index_move += 1
			if index_move == len_move:
				print ("\033[92mWIN")
				break
			space = 0

def first_draw(squareside, fenetre, blocks):
	i = 0
	while (i < (squareside*squareside)):
		utils.draw_block(blocks, fenetre, i)
		fenetre.blit(blocks[i].background, (blocks[i].x, blocks[i].y))
		pygame.draw.rect(fenetre, [238, 238, 224], (blocks[i].x, blocks[i].y, 100, 100), 1)
		pygame.display.update()
		i += 1

def call_game(ia_final_move, squareside, allcase, gamemode):
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	tiles = image_slicer.slice('/Users/gkuma/git/Npuzzle/photo.jpg', squareside*squareside, save=False)
	image_slicer.save_tiles(tiles, directory='/Users/gkuma/git/Npuzzle/', prefix='')
	blocks = []
	blocks = utils.build_board(allcase, squareside, blocks, fenetre)
	pygame.init()
	fond = pygame.image.load("/Users/gkuma/git/Npuzzle/background.jpg")
	fenetre.blit(fond, (0,0))
	pygame.display.flip()
	first_draw(squareside, fenetre, blocks)
	if gamemode == 'ia':
		main_loop(ia_final_move, squareside, fenetre, blocks, fond)
	if gamemode == 'solo':
		main_loop_solo(squareside, fenetre, blocks, fond)
