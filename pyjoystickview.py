#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Vinicius
  douglvini@gmail.com

  Distributed under the terms of GNU GPL v3 license.

This is a little program which show pressed buttons of a connected joystick.

"""

import pygame, math
pygame.init()

WINDOW_TITLE = "pygame Joystick View"

RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (120,120,120)
WHITE = (255,255,255)

class Sprite:
    def update(self,screen):
        pass

class Analog(Sprite):
    def __init__(self, pos, size=100):
        self.suport = None
        self.stick = None
        self.pos = pos
        self.size = size
        self._setup()
        self.axis_xy = (0,0)

    def _setup(self):
        size = self.size
        self.suport = pygame.Surface((size,size),pygame.SRCALPHA)
        self.stick = pygame.Surface((size/2,size/2),pygame.SRCALPHA)

        pygame.draw.circle(self.suport, GRAY, (size/2,size/2),size/2)
        pygame.draw.circle(self.stick, WHITE, (size/4,size/4),size/4)

    def update_axes(self, x, y):
        magnitude = math.sqrt((x*x) + (y*y))
        if magnitude > 1.0:
            x = x/magnitude
            y = y/magnitude
        self.axis_xy = (x, y)

    def update(self,screen):
        screen.blit(self.suport,self.pos)
        size = self.size
        pos = (self.pos[0] +  size/4 +  int(self.axis_xy[0] * (size/2)),
                self.pos[1] + size/4 + int(self.axis_xy[1] * (size/2))) 
        screen.blit(self.stick, pos)


class Text(Sprite):
    def __init__(self,text="Default",size=30):

        self.font = pygame.font.Font(None,size);
        self.text = self.font.render(text,0,(255,255,255))
        self.pos = (0,0)

    def setpos(self,pos=(0,0)):
        self.pos = pos

    def update_text(self,text,color=GREEN):
        self.text = self.font.render(text,0,color)

    def update(self,screen):
        screen.blit(self.text,self.pos)


class Application:
    def __init__(self,resolution=(800,600),font_size=30):
        self.is_running = False
        self.screen = None
        self.resolution = resolution
        self.objects = []
        self.font_size = font_size
        self.title_idx = 0
        self.joy = None

    def _setup(self):
        if (pygame.joystick.get_count() == 0):
            print("No Joystick plugged.")
            return False
        print("%i joystick(s) plugged."%(pygame.joystick.get_count()))
        self.joy = pygame.joystick.Joystick(0)
        self.joy.init()

        # setup screen
        self.screen = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption(WINDOW_TITLE)

        self._show_joystick()
        return True

    def _show_joystick(self):
        # buttons
        textpos = ((self.resolution[0]/2)-30 ,30)

        joysticks = Text(" ",self.font_size)
        self.objects.append(joysticks)
        self.title_idx = self.objects.index(joysticks)
        joysticks.setpos(textpos)
        height = 40 
        for i in range(self.joy.get_numbuttons()):
            text = Text(" ",self.font_size)
            height += self.font_size
            text.setpos((textpos[0],height))
            self.objects.append(text)
        
        # axes
        if (self.joy.get_numaxes() < 4):
            return
        analog_r = Analog((50,40))
        analog_l = Analog((50+150,40))
        self.objects.append(analog_r)
        self.objects.append(analog_l)

    def _update_axes(self):
        cnt = 0
        for i in range(0,len(self.objects)):
            if isinstance(self.objects[i], Analog):
                x = self.joy.get_axis(cnt)
                y = self.joy.get_axis(cnt+1)
                self.objects[i].update_axes(x,y)
                cnt += 2

    def _update_texts(self):
        self.objects[self.title_idx].update_text("buttons",RED)
        for i in range(0,len(self.objects)):
            if i != self.title_idx and isinstance(self.objects[i], Text):
                state = self.joy.get_button(i-1)

                color = GREEN
                if state == False: color = RED

                self.objects[i].update_text("%i: %r"%(i-1,state),color)

    def run(self):
        if not self._setup():
            return

        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False;

            self.screen.fill((0,0,0,0))
            self._update_texts()
            self._update_axes()
            for obj in self.objects:
                obj.update(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    app = Application()
    app.run()
