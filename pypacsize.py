#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2016, Douglas Knowman
  douglasknowman@gmail.com

  Distributed under the terms of GNU GPL v3 license.

Get the size of all istalled packets on arch linux distro.
"""

import subprocess, os
import time as t

LOG_NAMEPATH="./pacsize.log"

def process_packets():
    size = 0
    pacs = 0
    time = t.time()

    packages = subprocess.check_output(['pacman','-Qq']).splitlines()
    pacs = len(packages)
    cnt = 0
    sizecnt = 0

    for pack in packages:
        p = subprocess.check_output(['pacman','-Qi',pack]).decode('utf-8').splitlines()
        p = list(filter(lambda x: x[:len("Installed")] == "Installed",p))[0]
        pacsize = float(p[18:-3])
        m = p[-3:]
        if m == "KiB":
            pacsize = pacsize * (pow(1000,1)) 
        elif m == "MiB":
            pacsize = pacsize * (pow(1000,2))
        elif m == "GiB":
            pacsize = pacsize * (pow(1000,3))

        sizecnt += pacsize
        cnt +=1
        print ("[DONE] | %i%% | Analize %s"%(int((cnt/pacs) * 100),pack.decode('utf-8')))

    size = sizecnt / (pow(1000,3))
    time = t.time() - time
    return pacs,size,time

def save_log(date,npacs,size,time):
    logf = None
    if not os.path.exists(LOG_NAMEPATH):
        logf = open (LOG_NAMEPATH,'w')
    else : logf = open(LOG_NAMEPATH,'a')

    logs = "-- %s | analized %i packets in %.1f seconds, with %.3f GB\n"%(date,npacs,time,size)
    logf.write(logs)
    logf.close()
    print ("-- Log saved at %s"%LOG_NAMEPATH)

if __name__ == "__main__":
    pacs,size,time = process_packets()
    date = t.strftime("%D %H:%M")
    save_log(date,pacs,size,time)
    print("-- %s | %i packets processed in %.1f seconds, with size of %.3f GB"%(date, pacs, time, size))
