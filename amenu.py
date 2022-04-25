#! /bin/python
# -*- coding: utf-8 -*-
"""
#  file: amenu.py
#  license: GNU GPL v3(or lesser)
#  author: Douglas Vinicius
#  email: douglvini@gmail.com
#  date: 2017-12-10 -- 2022-04-22

"""
"""
This script will construct a vertical interactable menu that looks like this:
Category1:
    Program A
    Program B
Category2:
    Program C
    ...
"""
import subprocess, curses, os

MESSAGE = "amenu: <Enter> or <Space> to open a program, <q> to exit."

class Program:
    def __init__(self, name, execpath):
        self.name = name
        self.execpath = execpath

def parse_line(line):
    line = str(line.strip())
    name = ""
    kind = ""
    execpath = ""

    strings = line.split('"')
    name = strings[1]

    remain = strings[2].strip()
    has_execpath = remain.find(" ")
    if has_execpath != -1:
        kind = remain[:has_execpath]
        execpath = remain[has_execpath+1:-1]
    else:
        kind = remain[:-1]
    return (name, kind, execpath)

def main(screen):
    # parse the output of xdg_menu into the menu dictionary.
    # @todo check if xdg_menu exists before using it.
    menu = {}
    lines = subprocess.check_output(["xdg_menu"]).splitlines()[1:-1] # dont include the "Applications" menu.
    current_menu = ""
    end_level = 0
    program_count = 0
    for line in lines:
        name, kind, execpath = parse_line(line)
        if kind == "MENU":
            if current_menu == "": #if theres a sub menu ignore
                # @todo check for hash collisions
                current_menu = name
                menu[current_menu] = []
            end_level +=1
        elif kind == "END":
            end_level -= 1
            if end_level == 0:
                current_menu = ""
        elif kind == "EXEC":
            menu[current_menu].append(Program(name, execpath))
            program_count += 1

    # drawing the menu.
    top_pad = 2 # minimun 1
    left_pad = 2
    draw = curses.newpad(200, 200) #@cleanup rows shouldt be hardcoded.
    cursor_index = 0
    exec_program = False
    cursor_col = 0
    running = True
    while running:
        draw.clear()
        program_index = 0
        draw.addstr(0, left_pad, MESSAGE, curses.A_DIM)
        row_offset = 0
        for category, programs in menu.items():
            col_offset = 0
            draw.addstr(top_pad + row_offset, left_pad + col_offset, category, curses.A_DIM)
            col_offset = 4
            row_offset += 1
            for program in programs:
                attribute = 0
                if program_index == cursor_index:
                    attribute = curses.A_STANDOUT
                    cursor_col = top_pad + row_offset
                    if exec_program and program.execpath:
                        os.system("nohup " + program.execpath + "&")
                        exec_program = False
                        running = False
                draw.addstr(top_pad + row_offset, left_pad + col_offset, program.name, attribute)
                row_offset += 1
                program_index += 1

        row_count, col_count = screen.getmaxyx()

        # make the screen follow the cursor.
        offset = (cursor_col + 3) - row_count
        if offset < 0:
            offset = 0
        draw.refresh(offset, 0, 0, 0, row_count-1, col_count-1)
        screen.noutrefresh()

        if running: # @todo maybe input should be at the start of the loop.
            last_input = screen.getch() 
        if last_input == ord('j') or last_input == curses.KEY_DOWN:
            cursor_index += 1
        elif last_input == ord('k') or last_input == curses.KEY_UP:
            cursor_index -= 1
        elif last_input == ord(' ') or last_input == ord('\n'):
            exec_program = True

        # cursor_index = cursor_index % program_count
        cursor_index = max(0, min(program_count-1, cursor_index))

        # exiting if the user presses <q>
        if last_input == ord('q'):
            running = False

if __name__ == "__main__":
    # curses.wrapper(main)
    screen = curses.initscr()
    curses.curs_set(0)
    main(screen)
    # exiting...
    curses.endwin()
