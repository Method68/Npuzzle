#!/usr/bin/python
 
import pygame
from pygame.locals import *
pygame.init()

class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, font_size=30,
                    font_color=(255, 255, 255)):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
 
        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
 
            width = label.get_rect().width
            height = label.get_rect().height
 
            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
 
            self.items.append([item, label, (width, height), (posx, posy)])
 
    def run(self):
        mainloop = True
        choice = "NONE"
        choice_value = 0
        validate = 0
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        mainloop = False
                    if event.key == K_UP and choice_value < 2:
                        choice_value += 1
                        choice = self.items[choice_value][0]
                    elif event.key == K_DOWN and choice_value >= 0:
                        choice_value -= 1
                        choice = self.items[choice_value][0]
                    if event.key == 13:
                        validate = 1

            if validate == 1:
                print ("createa new submenue:")
                print (choice)
                break

            # Redraw the background
            self.screen.fill(self.bg_color)
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))
                print choice
                if name == choice:
                    self.screen.blit(self.font.render(('0-0-0'), 1, (255,0,0)), (posx + 100, posy))
            pygame.display.flip()

        #get the rigth value
        heuristic = 'Manhattan'
        algo = 'IDAstar'
        squareside = 4
        return heuristic, algo, squareside