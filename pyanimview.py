#! /usr/bin/env python2
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2016 Douglas Knowman <douglasknowman@gmail.com>
#
# Distributed under terms of the GNU GPL v3 license.

"""
this little app take a image of sprites and put on the screen
in sequence.

"""
import pygame
import sys

pygame.init()

VERSION = "0.1"
WINDOW_SIZE = (800,600)
BACKGROUND_COLOR = (0,0,0,255)

WINDOW_NAME = "Pygame Sprite Animation View [%s]" %VERSION
HELP_MSG = "\nCopyright (C) 2016 Douglas Knowman <douglasknowman@gmail.com> pyanimview v%s \npyanimview.py [image path] [grid width] [grid height] [sprite count] [framerate]\n" % VERSION

class AnimView:
    def __init__(self,spritepath,gridsize,spritecount,framerate=30):
        # basic view options
        self.screen  = None
        self.framerate = framerate
        self.gridsize = gridsize
        self.filepath = spritepath
        self.spritecount = spritecount
        
        self.clock = None
        self.is_running = False
        self.xcount = 0
        self.ycount = 0
        self.count = 0
        self.showsprite = None

        self.start_screen()
        self.loadSprite()

    def start_screen(self):
        # starting the screen and clock
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_NAME)
        self.clock = pygame.time.Clock()

    def loadSprite(self):
        # load sprite image, calculate the size of the frames and make a surface to blit to.
        self.sprite = pygame.image.load(self.filepath)
        self.sprite_framesize = (self.sprite.get_width() / self.gridsize[0], self.sprite.get_height() / self.gridsize[1])
        self.showsprite = pygame.Surface((self.sprite_framesize[0],self.sprite_framesize[1]))
    
    def start(self):
        print ">window open."
        self.is_running = True

        while self.is_running :
            self.clock.tick(self.framerate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            self.screen.fill (BACKGROUND_COLOR)
            # calculating position for crop the sprite image
            x = self.xcount * self.sprite_framesize[0]
            y = self.ycount * self.sprite_framesize[1]
            width = (self.xcount+1) * self.sprite_framesize[0]
            height = (self.ycount+1) * self.sprite_framesize[1]

            self.xcount += 1
            self.count += 1

            # get each frame from sprite image and render on surface with the best size
            self.showsprite.blit (self.sprite,(10,10),(x,y,width,height))

            # centralize the sprite frames
            centerx = (WINDOW_SIZE[0]/2) - self.sprite_framesize[0]/2
            centery = (WINDOW_SIZE[1]/2) - self.sprite_framesize[1]/2
            self.screen.blit (self.showsprite,(centerx,centery))

            # if the viewer show every frame then stop.
            if self.count == self.spritecount:
                self.xcount = 0
                self.ycount = 0

            if self.xcount == self.gridsize[0]:
                self.xcount = 0
                self.ycount += 1
                if self.ycount == self.gridsize[1]:
                    self.ycount = 0

            pygame.display.flip()
            
        pygame.quit()

def main():
    print (HELP_MSG)
    print "starting ..."
    if len(sys.argv) < 4:
        print "enter with correct arguments."
        return
    
    # scan argments
    spritepath = sys.argv[1]
    gridsize = (int(sys.argv[2]), int(sys.argv[3]))

    spritecount = int(sys.argv[4])
    if len(sys.argv) == 6: framerate = int(sys.argv[5])
    else: framerate = 30
    
    # start application class
    app = AnimView( spritepath,gridsize,spritecount,framerate)
    app.start()

if __name__ == "__main__":
    main()
