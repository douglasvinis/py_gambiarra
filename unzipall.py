#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Knowman
  douglasknowman@gmail.com

  Distributed under the terms of GNU GPL v3 (or lesser GPL) license.

script to unzip multiple 7z files with no or the same password.

"""
import glob,subprocess,sys
HELP = "Enter with a filepattern and a password if needed like ( unzipall.py [filenames] -p[password]"


def main():
    filenames = []
    filepass = None
    # check and parse the arguments
    if len(sys.argv) <= 1:
        print (HELP)
    else :
        for i in range(1,len(sys.argv)):
            if sys.argv[i][:2] == '-p':
                filepass = sys.argv[i][2:]
            else:
                filenames.append(sys.argv[i])


    # unzip all files with 7z and show on screen
    password = ''
    if filepass:
        password = '-p%s'%filepass

    for filename in filenames:
        print ("\n>----UNZIP----[ %s ]----UNZIP----<\n"%filename)
        subprocess.run(['7z','x',filename,password])

    # asks and remove extracted 7z files.
    rm = False
    ask = str(input("Do you wanna remove all 7z extracted files?(y,n): "))
    if ask == 'y':
        rm = True
    else :
        rm = False

    if rm:
        print ("\n>-----REMOVE ALL EXTRACTED FILES----<")
        for filename in filenames:
            subprocess.run(['rm',filename])
    # ending
    print ("Have a good one. :)")


if __name__ == "__main__":
    main()
