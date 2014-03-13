#!/usr/bin/python

import sys

oldx = [3e33, 3e33]
x = [3e33, 3e33]
delta = 0.6
lastblank = True

file = open(sys.argv[1],"r")
new = open(sys.argv[1].replace(".txt","") + "_new.txt","w")
for line in file:
    if line[0:1] == "#":
        new.write(line)
    elif line == "\n":
        oldx = [3e33, 3e33]
        if not lastblank:
            lastblank = True
            new.write("\n")
    else:
        s = line.split(" ")
        x[0] = float(s[0])
        x[1] = float(s[1])
        if oldx[0] == 3e33:
            oldx[0] = x[0]
            oldx[1] = x[1]
        d = abs(x[0]-oldx[0]) + abs(x[1]-oldx[1])
        new.write("{x} {y}\n".format(x=oldx[0], y=oldx[1]))
        if d > delta and not lastblank:
            print "inserting blank line"
            new.write("\n")
        lastblank = False
        oldx[0] = x[0]
        oldx[1] = x[1]

if oldx[0] != 3e33:
    new.write("{x} {y}\n".format(x=oldx[0], y=oldx[1]))
