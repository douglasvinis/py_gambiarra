#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2017, Douglas Vinicius
  douglvini@gmail.com

  Distributed under the terms of GNU GPL v3 (or lesser GPL) license.

  Create a raw disk img of a floppy disk (3.5i , 1.5Mb)
  and write the input files into the right Head,Cylinder,Sector.

"""
import os 
# place all data files to be written with the correct H,C,S information here
# Example:
#
# data = {
#   "filepath/filename": (head,cylinder,sector),
#   ...
#}
out_filename = "foo.img"
data = {
        "LICENSE":(0,0,0)
        }

# information about the floppy disk geometry
heads       = 2
cylinders   = 80
sectors     = 18

total_size = heads * cylinders * sectors * 512

def start():
    if len(data.keys()) == 0:
        print ("\n-> No data to write edit this file and put data on 'data' dictionary.")
        return

    disk_f = disk_create_empty()
    for key in data.keys():
        h,c,s = data[key]
        # open file data only for read
        print("-> begin to write file %s ..."%(key))
        data_f = open(key,'rb')
        disk_write(disk_f, h,c,s,data_f)
        data_f.close()
        print("-> done :)\n")
    disk_f.close()

def disk_create_empty():
    # open img file and write it with zeroes
    f = open(out_filename, 'wb')
    f.write(bytes(total_size))
    f.seek(0,0)

    print("\n-> Disk %s created with %.2fMb of size\n"%(out_filename,get_not(total_size,2)))
    return f

def disk_write(disk,h,c,s,f):
    f_size = get_filesize(f)

    print ("+= %8i byte(s) | %4.1fKb | %4.2fMb"%(f_size,
        get_not(f_size,1),
        get_not(f_size,2)))

    d_offset = get_byteoffset(h,c,s)
    disk.seek(d_offset,0)
    disk.write(f.read(f_size))

def get_byteoffset(h,c,s):
    # calculating the right position of the section on  the image.
    return ((h + 2*c) * sectors + s) * 512

def get_not(b, divpow):
    return b/(1024**divpow)

def get_filesize(f):
    f.seek(0,2)
    s = f.tell()
    f.seek(0,0)
    return s

if __name__ == "__main__":
    start()
