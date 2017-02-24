#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
        raise SystemExit("Sorry, extended image module required")

def main():
    pygame.init()
    fenetre = pygame.display.set_mode((640, 480), 0, 32)
    fond = pygame.image.load("/home/gabba/tmp_trash/puzzle-654962_1920.jpg").convert()
    fenetre.blit(fond, (0,0))
    pygame.display.flip()
    loop = 1
    totalsize = 4
    x = 0
    y = 0
    while loop:
        for event in pygame.event.get():
            if event.type == QUIT:
                loop = 0
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    print ("DOWN")
                    y += 25
                if event.key == K_UP:
                    print ("UP")
                    y -= 25
                if event.key == K_RIGHT:
                    print ("RIGHT")
                    x += 25
                if event.key == K_LEFT:
                    print ("LEFT")
                    x -= 25
        fenetre.blit(fond, (0,0))
        pygame.draw.rect(fenetre, (255,20,20), (x,y,40,80), 3)
        pygame.display.update()
        pygame.display.flip()
if __name__ == '__main__': main()
