#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Vinicius
  douglvini@gmail.com

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

    exit_codes = []
    for filename in filenames:
        print ("\n_________%s__________"%filename)
        exit_codes.append(subprocess.call(['7z','x',filename,password]))

    print ("\n___________[ Results of %i files ]____________\n"%len(filenames))
    for i in range(len(exit_codes)):
        result = "[DONE]"
        if (exit_codes[i] != 0):
            result = "[FAIL]"
        print("%s file: %s"%(result, filenames[i]))

    # asks and remove extracted 7z files.
    rm = False
    ask = str(input("\nDo you wanna remove all DONE extracted zip files? (y,n): "))
    if ask == 'y':
        rm = True
    else :
        rm = False

    if rm:
        done = len(list(filter(lambda x: x==0, exit_codes)))
        print ("\nremoving all %i extracted files!"%done)
        for i in range(len(filenames)):
            if (exit_codes[i] == 0):
                subprocess.run(['rm',filenames[i]])
    # ending
    print ("Have a good one!!")


if __name__ == "__main__":
    main()
