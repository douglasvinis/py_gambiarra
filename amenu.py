#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
#  file: amenu.py
#  license: GNU GPL v3(or lesser)
#  author: Douglas Vinicius
#  email: douglvini@gmail.com
#  date: 2017-12-10

"""
"""
this simple scripts needs xdg_menu installed in the machine. it uses curses
to make a interface with the user that can choose which app they want to open.
"""
import subprocess, curses, os

class Button:
    id = 0
    def __init__(self,screen, name, category, execpath, offset=[0,0]):
        self.name = name
        self.category = category
        self.execpath = execpath
        self.screen = screen
        self.offset = offset
        self.id = Button.id
        Button.id += 1

    def hi (self):
        self.screen.move (self.offset[0] + self.id, self.offset[1] + 0)
        curses.start_color()
        curses.init_pair(1,curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.screen.addstr("%-40s %s"%(self.name, self.category), curses.color_pair(1))
        self.screen.refresh()

    def normal (self):
        self.screen.move (self.offset[0] + self.id, self.offset[1] + 0)
        curses.start_color()
        curses.init_pair(2,curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.screen.addstr("%-40s %s"%(self.name, self.category), curses.color_pair(2))
        self.screen.refresh()

    def execute (self):
        #subprocess.call([self.execpath])
        os.system("nohup " + self.execpath + "&")

class Menu:
    def __init__(self, name):
        self.name = name
        self.buttons = []
        self.__setup()

    def __setup(self):
        self.screen = curses.initscr()
        curses.curs_set(False)

    def add_button (self, name, category, execpath):
        b = Button(self.screen, name, category, execpath,
                [2,2])
        b.normal()
        self.buttons.append(b)

    def run (self):
        key = None
        atual = 0
        while key != ord('q'):
            for i in range(len(self.buttons)):
                if i == atual:
                    self.buttons[atual].hi()
                else :
                    self.buttons[i].normal()
            key = self.screen.getch()
            if key == ord('j'):
                atual += 1
                if atual == len(self.buttons):
                    atual = 0
            elif key == curses.KEY_ENTER or key == 13 or key == 10:
                self.buttons[atual].execute()
                key = ord('q')
            elif key == ord('k'):
                atual -= 1
                if atual == -1:
                    atual = len(self.buttons)-1
        curses.endwin()

def get_string (s):
    inside = False
    string = ""
    for c in s:
        if c == "\"" and not inside:
            inside = True
            continue
        elif c == "\"" and inside:
            inside = False
            continue
        if inside:
            string += c
    return string

def find_string (s, word):
    pos = 0
    wp = 0
    for i in range(len(s)):
        if s[i] == word[wp]:
            wp += 1
        elif wp != 0:
            wp = 0

        if wp == len(word):
            return i - wp
    return 0


if __name__ == "__main__":
    lines = subprocess.check_output(["xdg_menu"]).splitlines()
    menu = Menu("Applications")
    atualmenu = ""
    for l in lines:
        l = str(l)
        if " MENU" in l:
            atualmenu = get_string(l)
        elif " EXEC" in l:
            pos = find_string(l, " EXEC")+ 5
            name = get_string(l)
            execpath = l[pos+1:-1]
            menu.add_button(name, atualmenu, execpath)
        elif " END" in l:
            atualmenu = ""
    menu.run()

