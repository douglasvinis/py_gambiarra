#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Vinicius
  douglvini@gmail.com

  Distributed under the terms of GNU GPL v3 license.

Get the size info of istalled packets on arch linux distro.
"""

import subprocess, os, sys
import time as t

LOG_NAMEPATH=os.path.expanduser('~')+"/pypacsize.log"
HELP="pypacsize -[actions]\n-[e] only installed by user packages\n"
HELP += "-[t] show and save a log of installed packages\n"
HELP += "-[l] list the size of each package\nexample: pypacsize -le || pypacsize -l\n"

def process_packets(explicit_installed=False):
    print(">scanning packages...")
    pacs_info = []
    time = t.time()

    if explicit_installed:
        pac_names = subprocess.check_output(['pacman','-Qeq']).splitlines()
        pac_sizes = subprocess.check_output("pacman -Qei|grep 'Installed Size'", shell=True).splitlines()
    else:
        pac_names = subprocess.check_output(['pacman','-Qq']).splitlines()
        pac_sizes = subprocess.check_output("pacman -Qi|grep 'Installed Size'", shell=True).splitlines()

    sizecnt = 0

    for i in range(len(pac_names)):
        name = pac_names[i]
        size = pac_sizes[i].decode('utf-8')[18:]

        size_bytes = float(size[:-3])
        power = size[-3:]

        exponent = 0
        if power == "KiB":
            exponent = 1
        elif power == "MiB":
            exponent = 2
        elif power == "GiB":
            exponent = 3
        else:
            size_bytes = float(size[:-2])

        size_bytes = size_bytes * pow(1000,exponent) 
        pacs_info.append([name.decode(), size_bytes, size])
        sizecnt += size_bytes

    print(">done.")
    size = sizecnt / pow(1000,3)
    time = t.time() - time
    print("> %d packages scanned in %.1f Seconds"%(len(pacs_info), time))
    return pacs_info,size,time

def save_log(msg, date,npacs,size,time):
    logf = None
    if not os.path.exists(LOG_NAMEPATH):
        logf = open (LOG_NAMEPATH,'w')
    else : logf = open(LOG_NAMEPATH,'a')

    logs = (msg+"\n")%(date,npacs,time,size)
    logf.write(logs)
    logf.close()
    print ("> Log saved at %s"%LOG_NAMEPATH)

def total_size(explicit_installed = False):
    pacs_info, size, time = process_packets(explicit_installed)
    date = t.strftime("%D %H:%M")
    explicit = " "
    if explicit_installed:
        explicit = "E"
    msg = "> %s |"+explicit+"| scanned %i packages in %.1f seconds, with total size of %.3f GB"
    save_log(msg,date,len(pacs_info),size,time)
    print(msg%(date,len(pacs_info),time, size))

def list_by_size(explicit_installed = False):
    packets, size, time = process_packets(explicit_installed)
    sorted_pacs = sorted(packets, key=lambda x: x[1], reverse=True)
    date = t.strftime("%D %H:%M")
    print(date)
    print("\n%-35s|%12s"%("PACKAGE","SIZE"))
    for packet in sorted_pacs:
        name = ("%s"%packet[0]).ljust(35, '-')
        print("%s|%12s"%(name,packet[2]))


if __name__ == "__main__":
    action = 0
    explicit = False
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if(arg[0] == '-'):
            for l in arg[1:]:
                if l == 't':
                    action = 0
                elif l == 'l':
                    action = 1
                elif l == 'e':
                    explicit = True
    print(HELP)
    actions = [total_size, list_by_size]
    actions[action](explicit)
