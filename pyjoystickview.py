#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Vinicius
  douglvini@gmail.com

  Distributed under the terms of GNU GPL v3 license.

This is a little program which show pressed buttons of a connected joystick.

"""

import pygame
pygame.init()

WINDOW_TITLE = "pygame Joystick View"

RED = (255,0,0)
GREEN = (0,255,0)

class Text:
    def __init__(self,text="Default",size=30):

        self.font = pygame.font.Font(None,size);
        self.text = self.font.render(text,0,(255,255,255))
        self._pos = (0,0)

    def set_pos(self,pos=(0,0)):
        self._pos = pos

    def update_text(self,text,color=GREEN):
        self.text = self.font.render(text,0,color)

    def update(self,screen):
        screen.blit(self.text,self._pos)

class Application:
    def __init__(self,resolution=(800,600),font_size=30):
        self.is_running = False
        self.screen = None
        self.resolution = resolution
        self.objects = []
        self.font_size = font_size
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        self.setup_screen()
        self.show_joystick()

    def setup_screen(self):
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(WINDOW_TITLE)

    def show_joystick(self):
        text_pos = ((self.resolution[0]/2)-20 ,20)
        joysticks = Text(" ",self.font_size)
        self.objects.append(joysticks)
        joysticks.set_pos(text_pos)
        height = 40 
        for i in range(self.joy.get_numbuttons()):
            text = Text(" ",self.font_size)
            height += self.font_size
            text.set_pos((text_pos[0],height))
            self.objects.append(text)

    def update_texts(self):
        self.objects[0].update_text("joysticks: %i" %pygame.joystick.get_count())
        for i in range(1,len(self.objects)):
            state = self.joy.get_button(i-1)

            color = GREEN
            if state == False: color = RED

            self.objects[i].update_text("button %i: %r"%(i-1,state),color)

    def start(self):
        self.is_running = True

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False;

            self.screen.fill((0,0,0,0))
            self.update_texts()
            for obj in self.objects:
                obj.update(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    app = Application()
    app.start()
