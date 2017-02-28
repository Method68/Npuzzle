import pygame
from pygame.locals import *
import utils
from utils import Block

# 
# Main loop work in progress
# 
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

def first_draw(squareside, fenetre, blocks):
	i = 0
	while (i < (squareside*squareside)):
		utils.draw_block(blocks, fenetre, i)
		fenetre.blit(blocks[i].body, (blocks[i].x, blocks[i].y))
		pygame.display.update()
		i += 1

def call_game(ia_final_move, squareside, allcase):
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	blocks = []
	blocks = utils.build_board(allcase, squareside, blocks, fenetre)
	pygame.init()
	# fond = pygame.image.load("/home/gabba/tmp_trash/puzzle-654962_1920.jpg").convert()
	# fenetre.blit(fond, (0,0))
	pygame.display.flip()
	first_draw(squareside, fenetre, blocks)
	main_loop(ia_final_move, squareside, fenetre, blocks)
