#import basic pygame modules
import pygame
from pygame.locals import *

blocksize = 50
tabposx = 150
tabposy = 150

class Rect(object):
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

def draw_block(rects, fenetre, i,):
	fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
	# block-border
	pygame.draw.rect(fenetre, [238, 238, 224], (rects[i].x, rects[i].y, 50, 50), 1)
	#display number
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render(rects[i].number, 1, (1,1,1))
	rects[i].body.blit(label, (15, 15))

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

def ia_move(ia_final_move, index_move, rects, squareside):
	if ia_final_move[index_move] == 'UP':
		key = K_UP
	if ia_final_move[index_move] == 'DOWN':
		key = K_DOWN
	if ia_final_move[index_move] == 'LEFT':
		key = K_LEFT
	if ia_final_move[index_move] == 'RIGHT':
		key = K_RIGHT
	rects = key_hook(rects, key, squareside)

def get_block_zero(blocks):
	block0 = blocks[0]
	for block in blocks:
		if block.number == '0':
			block0 = block
	return block0

def build_board(index, squareside, rects, fenetre):
	i = 0
	tmpx = tabposx
	tmpy = tabposy
	while (i < squareside*squareside):
		rects.append(Rect(fenetre, tmpx, tmpy, index[i]))
		if ((tmpx / ((squareside*blocksize - blocksize) + tabposx)) == 1.00):
			tmpx = tabposx
			tmpy += blocksize
		else:
			tmpx += blocksize
		i += 1
	return rects


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

def swap_values(rectx, rects):
	block0 = get_block_zero(rects)
	for new_rect in rects:
		if rectx.number == new_rect.number:
			tmpy = block0.y
			block0.y = new_rect.y
			new_rect.y = tmpy
			tmpx = block0.x
			block0.x = new_rect.x
			new_rect.x = tmpx
	return rects

def switch_rects(move, rects):
	block0 = get_block_zero(rects)
	for rect in rects:
		if move[1] == 'y':
			if ((move[0] == '+') and ((block0.y + blocksize) == rect.y) and ((block0.x) == rect.x)):
				rects = swap_values(rect, rects)
				break
			elif ((move[0] == '-') and ((block0.y - blocksize) == rect.y) and ((block0.x) == rect.x)):
				rects = swap_values(rect, rects)
				break
		elif move[1] == 'x':
			if ((move[0] == '+') and ((block0.x + blocksize) == rect.x) and ((block0.y) == rect.y)):
				rects = swap_values(rect, rects)
				break
			elif ((move[0] == '-') and ((block0.x - blocksize) == rect.x) and ((block0.y) == rect.y)):
				rects = swap_values(rect, rects)
				break
	return rects

def key_hook(rects, key, squareside):
	block0 = get_block_zero(rects)
	if key == K_DOWN:
		print ("DOWN")
		if (checkborder("+y", squareside, block0)):
			rects = switch_rects("+y", rects)
	elif key == K_UP:
		print ("UP")
		if (checkborder("-y", squareside, block0)):
			rects = switch_rects("-y", rects)
	elif key == K_RIGHT:
		print ("RIGHT")
		if (checkborder("+x", squareside, block0)):
			rects = switch_rects("+x", rects)
	elif key == K_LEFT:
		print ("LEFT")
		if (checkborder("-x", squareside, block0)):
			rects = switch_rects("-x", rects)
	return rects
