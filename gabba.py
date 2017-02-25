#!/usr/bin/env python

import random, os.path

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
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render(self.number, 1, (1,1,1))
		self.body.blit(label, (15, 15))

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

def swap_values(rect0, rectx, rects):
	for new_rect in rects:
		if rectx.number == new_rect.number:
			tmpy = rects[0].y
			rects[0].y = new_rect.y
			new_rect.y = tmpy
			tmpx = rects[0].x
			rects[0].x = new_rect.x
			new_rect.x = tmpx
	return rects

def switch_rects(move, rects):
	print " !!!  value of rects[0].x:"+str(rects[0].x)+" rects[0].y:"+str(rects[0].y)
	print "move:"+move
	for rect in rects:
		print "value of rect.x:"+str(rect.x)+" rect.y:"+str(rect.y) 
		if move[1] == 'y':
			if ((move[0] == '+') and ((rects[0].y + blocksize) == rect.y) and ((rects[0].x) == rect.x)):
				rects = swap_values(rects[0], rect, rects)
				break
			elif ((move[0] == '-') and ((rects[0].y - blocksize) == rect.y) and ((rects[0].x) == rect.x)):
				rects = swap_values(rects[0], rect, rects)
				break
		elif move[1] == 'x':
			if ((move[0] == '+') and ((rects[0].x + blocksize) == rect.x) and ((rects[0].y) == rect.y)):
				rects = swap_values(rects[0], rect, rects)
				break
			elif ((move[0] == '-') and ((rects[0].x - blocksize) == rect.x) and ((rects[0].y) == rect.y)):
				rects = swap_values(rects[0], rect, rects)
				break
	return rects

def key_hook(rects, key, squareside):
	if key == K_DOWN:
		print ("DOWN")
		if (checkborder("+y", squareside, rects[0])):
			rects = switch_rects("+y", rects)
	elif key == K_UP:
		print ("UP")
		if (checkborder("-y", squareside, rects[0])):
			rects = switch_rects("-y", rects)
	elif key == K_RIGHT:
		print ("RIGHT")
		if (checkborder("+x", squareside, rects[0])):
			rects = switch_rects("+x", rects)
	elif key == K_LEFT:
		print ("LEFT")
		if (checkborder("-x", squareside, rects[0])):
			rects = switch_rects("-x", rects)
	return rects

def build_board(squareside, rects, fenetre):
	i = 0
	tmpx = tabposx
	tmpy = tabposy
	while (i < squareside*squareside):
		print (i)
		rects.append(Rect(fenetre, tmpx, tmpy, i))
		if ((tmpx / (150 + tabposx)) == 1.00):
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
	squareside = 4
	rects = []
	rects = build_board(squareside, rects, fenetre)
	while loop:
		for event in pygame.event.get():
			if event.type == QUIT:
				loop = 0
			if event.type == KEYDOWN:
				rects = key_hook(rects, event.key, squareside)

		# fenetre.blit(fond, (0,0))
		i = 0
		while (i < (squareside*squareside)):
			fenetre.blit(rects[i].body, (rects[i].x, rects[i].y))
			pygame.draw.rect(fenetre, [238, 238, 224], (rects[i].x, rects[i].y, 50, 50), 1)
			i += 1
		fenetre.blit(rects[0].body, (rects[0].x, rects[0].y))
		pygame.display.update()
		pygame.display.flip()

if __name__ == '__main__': main()
