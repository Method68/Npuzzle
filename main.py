#!/usr/bin/env python

import random, os.path

import core_solver

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
		raise SystemExit("Sorry, extended image module required")

blocksize = 50
tabposx = 150
tabposy = 150

class Rect(object):
	"""__init__() functions as the class constructor"""
	def __init__(self, fenetre=None, x=None, y=None, i=None):
		print ("obj"+str(i))
		if i == 0:
			print ("i = 0")
			self.color = (180, 205, 205)
		else :
			# self.color = (((i * 3)+150, (i * 4)+150, (i * 1)+150))
			self.color = (255, 255, 255)
		self.x = x
		self.y = y
		self.body = pygame.Surface((blocksize,blocksize))
		self.body.fill(self.color)
		self.number = str(i)
		# print ("My number is")
		# print (self.number)

def checkborder(index, squareside, rect0):
	if index[1] == 'y':
		if ((index[0] == '+') and ((rect0.y + blocksize) == tabposy + squareside*blocksize)):
			return 0
		if ((index[0] == '-') and ((rect0.y) == tabposy)):
			return 0
	elif index[1] == 'x':
		if ((index[0] == '+') and ((rect0.x + blocksize) == tabposx + squareside*blocksize)):
			return 0
		if ((index[0] == '-') and ((rect0.x) == tabposx)):
			return 0
	return 1	

def swap_values(rectx, rects):
	rect0 = rects[0]
	for rect in rects:
		if rect.number == '0':
			rect0 = rect
	for new_rect in rects:
		if rectx.number == new_rect.number:
			tmpy = rect0.y
			rect0.y = new_rect.y
			new_rect.y = tmpy
			tmpx = rect0.x
			rect0.x = new_rect.x
			new_rect.x = tmpx
	return rects

def switch_rects(move, rects):
	# print " !!!  value of rects[0].x:"+str(rects[0].x)+" rects[0].y:"+str(rects[0].y)
	# print "move:"+move
	rect0 = rects[0]
	for rect in rects:
		if rect.number == '0':
			rect0 = rect
	for rect in rects:
		if move[1] == 'y':
			if ((move[0] == '+') and ((rect0.y + blocksize) == rect.y) and ((rect0.x) == rect.x)):
				rects = swap_values(rect, rects)
				break
			elif ((move[0] == '-') and ((rect0.y - blocksize) == rect.y) and ((rect0.x) == rect.x)):
				rects = swap_values(rect, rects)
				break
		elif move[1] == 'x':
			if ((move[0] == '+') and ((rect0.x + blocksize) == rect.x) and ((rect0.y) == rect.y)):
				rects = swap_values(rect, rects)
				break
			elif ((move[0] == '-') and ((rect0.x - blocksize) == rect.x) and ((rect0.y) == rect.y)):
				rects = swap_values(rect, rects)
				break
	return rects

def key_hook(rects, key, squareside):
	rect0 = rects[0]
	for rect in rects:
		# print "print rect info 1"
		# print rect.number
		if rect.number == '0':
			# print "print rect info"
			# print rect0.x
			# print rect0.y
			# print rect0.number
			rect0 = rect
	if key == K_DOWN:
		print ("DOWN")
		if (checkborder("+y", squareside, rect0)):
			rects = switch_rects("+y", rects)
	elif key == K_UP:
		print ("UP")
		if (checkborder("-y", squareside, rect0)):
			rects = switch_rects("-y", rects)
	elif key == K_RIGHT:
		print ("RIGHT")
		if (checkborder("+x", squareside, rect0)):
			rects = switch_rects("+x", rects)
	elif key == K_LEFT:
		print ("LEFT")
		if (checkborder("-x", squareside, rect0)):
			rects = switch_rects("-x", rects)
	return rects

def build_board(index, squareside, rects, fenetre):
	i = 0
	tmpx = tabposx
	tmpy = tabposy
	while (i < squareside*squareside):
		# print (i)
		# print (index[i])
		rects.append(Rect(fenetre, tmpx, tmpy, index[i]))
		if ((tmpx / ((squareside*blocksize - blocksize) + tabposx)) == 1.00):
			tmpx = tabposx
			tmpy += blocksize
		else:
			tmpx += blocksize
		i += 1
	return rects

def main():
	pygame.init()
	fenetre = pygame.display.set_mode((800, 600), 0, 32)
	# fond = pygame.image.load("/home/gabba/tmp_trash/puzzle-654962_1920.jpg").convert()
	# fenetre.blit(fond, (0,0))
	pygame.display.flip()
	loop = 1
	squareside = input('\033[92mChoose size for Npuzzle: \n')

	width = int(squareside)
	solvable = None
	while (solvable == None):
		allvalue = width * width
		#list trier pour le tableau de fin
		allcase_order = [x for x in range(0, allvalue)]
		#list random pour le tableau de jeu
		allcase = random.sample(range(allvalue),allvalue)

		#Cree un tableau a 2 dimension pour le tableau a atteindre fin du jeu
		finalboard = []
		k = 0
		for i in range(width):
			new = []
			for j in range(width):
				new.append(allcase_order[k])
				k += 1
			finalboard.append(new)

		#Cree un tableau a 2 dimension pour le plateau de jeu
		gameboard = []
		order= []
		k = 0
		for i in range(width):
			new = []
			for j in range(width):
				new.append(allcase[k])
				k += 1
			gameboard.append(new)

		solvable = core_solver.construct(squareside, gameboard, finalboard)
		if (solvable != None):
			rects = []
			rects = build_board(allcase, squareside, rects, fenetre)
			print ("Board Builded")
			ia_final_move = solvable
			print solvable
		else:
			print ("Board Not Builded")

	len_move = len(ia_final_move)
	index_move = 0
	space = 0
	# rects = key_hook(rects, event.key, squareside)
	i = 0
	while (i < (squareside*squareside)):
		print "HERE"
		# block-body
		fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
		# block-border
		pygame.draw.rect(fenetre, [238, 238, 224], (rects[i].x, rects[i].y, 50, 50), 1)
		#display number
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(rects[i].number, 1, (1,1,1))
		rects[i].body.blit(label, (15, 15))
		fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
		pygame.display.update()
		i += 1

	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				loop = 0
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					space = 1
				rects = key_hook(rects, event.key, squareside)

		if space == 1:

			#ia move
			if ia_final_move[index_move] == 'UP':
				key = K_UP
			if ia_final_move[index_move] == 'DOWN':
				key = K_DOWN
			if ia_final_move[index_move] == 'LEFT':
				key = K_LEFT
			if ia_final_move[index_move] == 'RIGHT':
				key = K_RIGHT
			rects = key_hook(rects, key, squareside)
			# fenetre.blit(fond, (0,0))
			
			i = 0
			while (i < (squareside*squareside)):
				# block-body
				fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
				# block-border
				pygame.draw.rect(fenetre, [238, 238, 224], (rects[i].x, rects[i].y, 50, 50), 1)
				#display number
				myfont = pygame.font.SysFont("monospace", 15)
				label = myfont.render(rects[i].number, 1, (1,1,1))
				rects[i].body.blit(label, (15, 15))
				i += 1

			rect0 = rects[0]
			for rect in rects:
				if rect.number == '0':
					rect0 = rect
			fenetre.blit(rect0.body, (rect0.x, rect0.y))
			pygame.display.update()
			# pygame.display.flip()
			index_move += 1
			if index_move == len_move:
				break
			space -= 1
	print "WIN"
	while loop:
		loop = 1

if __name__ == '__main__': main()
