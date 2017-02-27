#import basic pygame modules
import pygame
from pygame.locals import *

blocksize = 50
tabposx = 150
tabposy = 150

class Block(object):
	"""__init__() functions as the class constructor"""
	def __init__(self, fenetre=None, x=None, y=None, i=None):
		if i == 0:
			self.color = (180, 205, 205)
		else :
			# self.color = (((i * 3)+150, (i * 4)+150, (i * 1)+150))
			self.color = (255, 255, 255)
		self.x = x
		self.y = y
		self.body = pygame.Surface((blocksize, blocksize))
		self.body.fill(self.color)
		self.number = str(i)

def draw_block(blocks, fenetre, i,):
	fenetre.blit(blocks[i].body, (blocks[i].x, blocks[i].y))
	# block-border
	pygame.draw.rect(fenetre, [238, 238, 224], (blocks[i].x, blocks[i].y, 50, 50), 1)
	#display number
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render(blocks[i].number, 1, (1,1,1))
	blocks[i].body.blit(label, (15, 15))

def set_board(liste, width):
	board = []
	k = 0
	for i in range(width):
		new = []
		for j in range(width):
			new.append(liste[k])
			k += 1
		board.append(new)
	return board

def ia_move(ia_final_move, index_move, blocks, squareside):
	if ia_final_move[index_move] == 'UP':
		key = K_UP
	if ia_final_move[index_move] == 'DOWN':
		key = K_DOWN
	if ia_final_move[index_move] == 'LEFT':
		key = K_LEFT
	if ia_final_move[index_move] == 'RIGHT':
		key = K_RIGHT
	blocks = key_hook(blocks, key, squareside)

def get_block_zero(blocks):
	block0 = blocks[0]
	for block in blocks:
		if block.number == '0':
			block0 = block
	return block0

def build_board(index, squareside, blocks, fenetre):
	i = 0
	tmpx = tabposx
	tmpy = tabposy
	while (i < squareside*squareside):
		blocks.append(Block(fenetre, tmpx, tmpy, index[i]))
		if ((tmpx / ((squareside*blocksize - blocksize) + tabposx)) == 1.00):
			tmpx = tabposx
			tmpy += blocksize
		else:
			tmpx += blocksize
		i += 1
	return blocks


def checkborder(index, squareside, block0):
	if index[1] == 'y':
		if ((index[0] == '+') and ((block0.y + blocksize) == tabposy + squareside*blocksize)):
			return 0
		if ((index[0] == '-') and ((block0.y) == tabposy)):
			return 0
	elif index[1] == 'x':
		if ((index[0] == '+') and ((block0.x + blocksize) == tabposx + squareside*blocksize)):
			return 0
		if ((index[0] == '-') and ((block0.x) == tabposx)):
			return 0
	return 1	

def swap_values(rectx, blocks):
	block0 = get_block_zero(blocks)
	for new_rect in blocks:
		if rectx.number == new_rect.number:
			tmpy = block0.y
			block0.y = new_rect.y
			new_rect.y = tmpy
			tmpx = block0.x
			block0.x = new_rect.x
			new_rect.x = tmpx
	return blocks

def switch_blocks(move, blocks):
	block0 = get_block_zero(blocks)
	for rect in blocks:
		if move[1] == 'y':
			if ((move[0] == '+') and ((block0.y + blocksize) == rect.y) and ((block0.x) == rect.x)):
				blocks = swap_values(rect, blocks)
				break
			elif ((move[0] == '-') and ((block0.y - blocksize) == rect.y) and ((block0.x) == rect.x)):
				blocks = swap_values(rect, blocks)
				break
		elif move[1] == 'x':
			if ((move[0] == '+') and ((block0.x + blocksize) == rect.x) and ((block0.y) == rect.y)):
				blocks = swap_values(rect, blocks)
				break
			elif ((move[0] == '-') and ((block0.x - blocksize) == rect.x) and ((block0.y) == rect.y)):
				blocks = swap_values(rect, blocks)
				break
	return blocks

def key_hook(blocks, key, squareside):
	block0 = get_block_zero(blocks)
	if key == K_DOWN:
		print ("DOWN")
		if (checkborder("+y", squareside, block0)):
			blocks = switch_blocks("+y", blocks)
	elif key == K_UP:
		print ("UP")
		if (checkborder("-y", squareside, block0)):
			blocks = switch_blocks("-y", blocks)
	elif key == K_RIGHT:
		print ("RIGHT")
		if (checkborder("+x", squareside, block0)):
			blocks = switch_blocks("+x", blocks)
	elif key == K_LEFT:
		print ("LEFT")
		if (checkborder("-x", squareside, block0)):
			blocks = switch_blocks("-x", blocks)
	return blocks
