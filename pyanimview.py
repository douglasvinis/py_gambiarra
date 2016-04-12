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

WINDOW_NAME = "Pygame Sprite Animation View [%s]" %VERSION
HELP_MSG = "\nCopyright (C) 2016 Douglas Knowman <douglasknowman@gmail.com> pyanimview v%s \npyanimview.py [image path] [grid width] [grid height] [framerate]\n" % VERSION

class AnimView:
    def __init__(self,spritepath,gridsize,framerate=30):
        # basic view options
        self.screen  = None
        self.framerate = framerate
        gridsize = gridsize
        self.filepath = spritepath
        
        self.clock = None
        self.is_running = False

        

    def start_screen(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_NAME)
        self.clock = pygame.time.Clock()
    
    def start(self):
        print ">window open."
        self.is_running = True
            
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

    if len(sys.argv) == 5: framerate = int(sys.argv[4])
    else: framerate = 30
    
    # start application class
    #app = AnimView( spritepath,gridsize,framerate)
    #app.start()

if __name__ == "__main__":
    main()
