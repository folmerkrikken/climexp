#!/usr/bin/python

import sys

firstx = [3e33, 3e33]
oldx = [3e33, 3e33]
x = [3e33, 3e33]
delta = 0.1
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
            firstx[0] = x[0]
            firstx[1] = x[1]
    else:
        s = line.split(" ")
        x[0] = float(s[0])
        x[1] = float(s[1])
        if firstx[0] == 3e33:
            new.write("# inserted breaks when points are more than %f degrees apart\n" % delta)
            firstx[0] = x[0]
            firstx[1] = x[1]
        if oldx[0] == 3e33:
            oldx[0] = x[0]
            oldx[1] = x[1]
        d = abs(x[0]-oldx[0]) + abs(x[1]-oldx[1])
        d1 = abs(oldx[0]-firstx[0]) + abs(oldx[1]-firstx[1])
        new.write("{x} {y}\n".format(x=oldx[0], y=oldx[1]))
        if d > delta and d1 < delta and not lastblank:
            print "inserting blank line"
            new.write("\n")
            firstx[0] = x[0]
            firstx[1] = x[1]
        lastblank = False
        oldx[0] = x[0]
        oldx[1] = x[1]

if oldx[0] != 3e33:
    new.write("{x} {y}\n".format(x=oldx[0], y=oldx[1]))
