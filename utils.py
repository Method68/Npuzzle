#import basic pygame modules
import pygame
from pygame.locals import *
from resizeimage import resizeimage
from core_solver import set_finalboard, set_board

blocksize = 100
tabposx = 50
tabposy = 50

class Block(object):
	"""__init__() functions as the class constructor"""
	def __init__(self, poscursor, squareside, photo, fenetre=None, x=None, y=None, i=None):
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
		if (i == poscursor):
			self.iscursor = 1
		else:
			self.iscursor = 0
		self.background = pygame.image.load("/Users/gkuma/git/Npuzzle/"+photo)

def return_pos_image(index, indexi, squareside):
	# gameboard = set_board(index, squareside)
	finalboard = set_finalboard(squareside)
	for raw in range(squareside):
		for col in range(squareside):
			if (finalboard[raw][col] == indexi):
				nbrraw = str(raw+1)
				nbrcol = str(col+1)
				if (raw < 10):
					nbrraw = "0"+nbrraw
				if (col < 10):
					nbrcol = "0"+nbrcol
				imagename = "_"+str(nbrraw)+"_"+str(nbrcol)+".png"
				return imagename

def build_board(index, squareside, blocks, fenetre):
	i = 0
	poscursor = 0
	tmpx = tabposx
	tmpy = tabposy
	for value in index:
		if (value == 0):
			poscursor = value
	while (i < squareside*squareside):
		image_name = return_pos_image(index, index[i], squareside)

		blocks.append(Block(poscursor, squareside, image_name, fenetre, tmpx, tmpy, index[i]))
		if ((tmpx / ((squareside*blocksize - blocksize) + tabposx)) == 1.00):
			tmpx = tabposx
			tmpy += blocksize
		else:
			tmpx += blocksize
		i += 1
	return blocks

def draw_block(blocks, fenetre, i,):
	fenetre.blit(blocks[i].background, (blocks[i].x, blocks[i].y))
	pygame.draw.rect(fenetre, [238, 238, 224], (blocks[i].x, blocks[i].y, 100, 100), 1)

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

def player_move(ia_final_move, index_move, blocks, squareside, new_gameboard):
	if ia_final_move[index_move] == 'UP':
		key = K_UP
	if ia_final_move[index_move] == 'DOWN':
		key = K_DOWN
	if ia_final_move[index_move] == 'LEFT':
		key = K_LEFT
	if ia_final_move[index_move] == 'RIGHT':
		key = K_RIGHT
	blocks, new_gameboard = key_hook(blocks, key, squareside, new_gameboard)
	return blocks, new_gameboard

def get_block_zero(blocks):
	for block in blocks:
		print ("block.number = "+ str(block.number))
		if block.iscursor == 1:
			print ("ok")
			block0 = block
			break
	return block0

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

def swap_values(rectx, blocks, new_gameboard):
	block0 = get_block_zero(blocks)
	
	print ("block0 : " +str(block0.number))

	print ("block0 : " + str(block0.x)+" "+ str(block0.y)+" "+ str(block0.number))
	for new_rect in blocks:
		if rectx.x == new_rect.x and rectx.y == new_rect.y:
			print ("new_rect : " + str(new_rect.x)+" "+ str(new_rect.y)+" "+ str(new_rect.number))
			tmpy = block0.y
			block0.y = new_rect.y
			new_rect.y = tmpy

			tmpx = block0.x
			block0.x = new_rect.x
			new_rect.x = tmpx

			raw = int((new_rect.x-50)/100)
			col = int((new_rect.y-50)%100)
			print ("block0 : " + str(block0.x)+" "+ str(block0.y)+" "+ str(block0.number))
			print ("new_rect : " + str(new_rect.x)+" "+ str(new_rect.y)+" "+ str(new_rect.number))

	# block0raw = int((block0.x-50)/100)
	# block0col = int((block0.y-50)%100)
	# print ("new rect raw"+str(raw))
	# print ("new rect col"+str(col))
	# print ("block0 raw"+str(block0raw))
	# print ("block0 col"+str(block0col))
	# print (new_gameboard)
	# new_gameboard[raw][col] , new_gameboard[block0raw][block0col] = new_gameboard[block0raw][block0col], new_gameboard[raw][col]
	new_gameboard = new_gameboard
	return blocks, new_gameboard

def switch_blocks(move, blocks, new_gameboard):
	block0 = get_block_zero(blocks)
	for rect in blocks:
		if move[1] == 'x':
			if ((move[0] == '+') and ((block0.x + blocksize) == rect.x) and (block0.y == rect.y)):
				blocks, new_gameboard = swap_values(rect, blocks, new_gameboard)
				print ("+x")
				break
			elif ((move[0] == '-') and ((block0.x - blocksize) == rect.x) and (block0.y == rect.y)):
				blocks, new_gameboard = swap_values(rect, blocks, new_gameboard)
				print ("-x")
				break
		elif move[1] == 'y':
			if ((move[0] == '+') and ((block0.y + blocksize) == rect.y) and (block0.x == rect.x)):
				blocks, new_gameboard = swap_values(rect, blocks, new_gameboard)
				print ("+y")
				break
			elif ((move[0] == '-') and ((block0.y - blocksize) == rect.y) and (block0.x == rect.x)):
				blocks, new_gameboard = swap_values(rect, blocks, new_gameboard)
				print ("-y")
				break
	return blocks, new_gameboard

def key_hook(blocks, key, squareside, new_gameboard):
	block0 = get_block_zero(blocks)
	if key == K_DOWN:
		if (checkborder("+y", squareside, block0)):
			blocks, new_gameboard = switch_blocks("+y", blocks, new_gameboard)
	elif key == K_UP:
		if (checkborder("-y", squareside, block0)):
			blocks, new_gameboard = switch_blocks("-y", blocks, new_gameboard)
	elif key == K_RIGHT:
		if (checkborder("+x", squareside, block0)):
			blocks, new_gameboard = switch_blocks("+x", blocks, new_gameboard)
	elif key == K_LEFT:
		if (checkborder("-x", squareside, block0)):
			blocks, new_gameboard = switch_blocks("-x", blocks, new_gameboard)
	return blocks, new_gameboard
