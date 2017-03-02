import pygame
from pygame.locals import *
import utils
from utils import Block
import menu
from menu import GameMenu

# 
# Main loop work in progress
# 

def main_loop_solo(squareside, fenetre, blocks):
	index_move = 0
	loop = 1
	space = 0
	ia_final_move = 0
	move = []
	movelen = 0
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
				movelen = 1
			elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				loop = 0
		if movelen == 1 and len(move) > 0:
			utils.ia_move(move, 0, blocks, squareside)
			i = 0
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			fenetre.blit(block0.body, (block0.x, block0.y))
			pygame.display.update()
			lenmove = 0
			move = []

def main_loop(ia_final_move, squareside, fenetre, blocks):
	len_move = len(ia_final_move)
	index_move = 0
	loop = 1
	space = 0
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
		#use space to see the next step
		if space == 1 and len_move > 0:
			utils.ia_move(ia_final_move, index_move, blocks, squareside)
			# display an background images
			fenetre.blit(fond, (0,0))
			i = 0
			while (i < (squareside*squareside)):
				utils.draw_block(blocks, fenetre, i)
				i += 1
			block0 = utils.get_block_zero(blocks)
			fenetre.blit(block0.body, (block0.x, block0.y))
			pygame.display.update()
			# for fenetre font
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
# 				#load the image to a surface
# #create a rect half the width of the image
# half_rect = pygame.rect(blocks.background.width/2, blocks.background.height/2)
# #blit first half

# fenetre.blit((0,0), half_rect, blocks.background)
# #blit second half
# fenetre.blit((image.width+10,0),half_rect, blocks.background)

		fenetre.blit(blocks[i].body, (blocks[i].x, blocks[i].y))
		pygame.display.update()
		i += 1

def call_game(ia_final_move, squareside, allcase, gamemode):
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	tiles = image_slicer.slice('photo.jpg', 4, save=False)
	image_slicer.save_tiles(tiles, directory='~/photo', prefix='slice', ext='jpg')
	blocks = []
	blocks = utils.build_board(allcase, squareside, blocks, fenetre)
	pygame.init()
	fond = pygame.image.load("/Users/gkuma/git/Npuzzle/background.jpg")
	fenetre.blit(fond, (0,0))
	pygame.display.flip()
	first_draw(squareside, fenetre, blocks)
	if gamemode == 'ia':
		main_loop(ia_final_move, squareside, fenetre, blocks)
	if gamemode == 'solo':
		main_loop_solo(squareside, fenetre, blocks)
