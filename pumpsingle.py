# -*- coding: utf-8 -*-

'''
    pump-single module
'''

# stuff to make compatible with Python 2 and 3
from __future__ import print_function
from builtins import input
from io import open

from random import randint, choice
import sys, codecs, argparse

try: # Python 2
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError: # Python 3
    from tkinter import *
    from tkinter import filedialog

# ~~~~~ Configure these settings! ~~~~~
#afronova_off = False # disables afronova walk (hopefully i'll make it a chance later)
random = False # completely random arrows, ignores patterns
overwrite_with_hold_ends = False # if hold end gets in the way of algorithm, overwrite the note that would be there (False means that it will try to move the arrow to another spot)

same_arrow_limit = 3 # configure how many of the same arrow can happen in a row (such that footswitches and jacks are disabled)
disable_footswitches_with_jacks = True # disable footswitches and jacks occurring one after the other

# Weights: Configure how often you want certain patterns to occur as a decimal
# Note that if conditions are unmet for a pattern to occur, it will ignore the pattern (meaning it may happen less than expected)
crossovers = 0.1
spins = 0.0 # this doesn't necessarily mean a full spin
footswitches = 0.5
jacks = 0.0
repeats = 0.1 # drills, triples, etc.

# Disable patterns at certain fraction
fenable = True
fthreshold = 16 # put reciprocal of fraction (1/16 is 16 or 16/1)
fdisable_crossovers = True
fdisable_spins = True
fdisable_footswitches = True
fdisable_jacks = True
fdisable_repeats = False

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def generate(note): # NOTE: prevent jacks or repeats when hold is still happening
    new = []
    L, R = Llast, Rlast = Lsafe, Rsafe = 0, 4
    Lcount, Rcount = 0, 0
    last = 0
    leftfoot = bool(randint(0,1))
    realleftfoot = leftfoot
    lastset = [1,0,0,0,0]
    fullholdlist = []
    lastp = []
    for a in range(len(note)):
        temp = []
        lastmove = -1
        count = 0
        for b in range(len(note[a])):
            if note[a][b] == len(note[a][b]) * note[a][b][0]:
                temp.append("000000000")
                continue
            nextlist = []
            holdlist = []
            rolllist = []
            endlist = []
            minelist = []
            realleftfoot = leftfoot
            if float(b-lastmove)/len(note[a]) <= (1/fthreshold) and (b-lastmove) >= 0: # if fraction threshold passed disable stuff
                #print("it happened")
                f_c = fdisable_crossovers
                f_s = fdisable_spins
                f_f = fdisable_footswitches
                f_j = fdisable_jacks
                f_r = fdisable_repeats
            else:
                f_c = f_s = f_f = f_j = f_r = False
            if disable_footswitches_with_jacks:
                if lastp == ['footswitches']:
                    f_j = True
                elif lastp == ['jacks']:
                    f_f = True
            if count >= same_arrow_limit+1 or count >= same_arrow_limit+1:
                f_j = True
                f_f = True
            for c in range(note[a][b].count('1')+note[a][b].count('2')+note[a][b].count('4')): # gets all arrows
                next = [0,1,2,3,4]
                for d in nextlist:
                    next.remove(d)
                if random:
                    n = randint(0,4)
                elif not random:
                    patterns =  ['normal']*int(100*normal) + \
                                ['crossovers']*int(100*crossovers*int(not f_c)) + \
                                ['spins']*int(100*spins*int(not f_s)) + \
                                ['footswitches']*int(100*footswitches*int(not f_f)) + \
                                ['jacks']*int(100*jacks*int(not f_j)) + \
                                ['repeats']*int(100*repeats*int(not f_r))
                    p = choice(patterns)
                    if p == 'normal': # to do: put all of these in functions to reduce redundant code
                        if L == 4 and R == 0:
                            if leftfoot: # 0,1,2
                                if Lsafe not in nextlist:
                                    next = [Lsafe]
                                else: # jumps are way different in pump so i need to fix (such that if more than 2 arrows then not 0 and 1 or not 4 and 5 unless 2)
                                    tmpft = [x for x in range(0,5) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else: # 1,2,3
                                if Rsafe not in nextlist:
                                    next = [Rsafe]
                                else:
                                    tmpft = [x for x in range(0,5) if x not in nextlist]
                                    next = [choice(tmpft)]
                        elif leftfoot: # 0,1,2
                            if R == 0: # go back to last arrow
                                if L not in nextlist:
                                    next = [L]
                                else:
                                    tmpft = [x for x in range(0,5) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else:
                                if len(nextlist):
                                    tmpft = [x for x in range(0,5) if x not in nextlist]
                                    next = [choice(tmpft)]
                                else:
                                    if 3 in next:
                                        next.remove(3)
                                    if 4 in next:
                                        next.remove(4)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                        else: # 1,2,3
                            if L == 3:  # go back to last arrow
                                if R not in nextlist:
                                    next = [R]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else:
                                if len(nextlist):
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                                else:
                                    if 0 in next:
                                        next.remove(0)
                                    if 1 in next:
                                        next.remove(1)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                    elif p == 'crossovers': # this will not start a crossover if it just happened (unless afronova walk)
                        if L == 3 and R == 0:
                            if leftfoot: # 0,1,2
                                if Lsafe not in nextlist:
                                    next = [Lsafe]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else: # 1,2,3
                                if Rsafe not in nextlist:
                                    next = [Rsafe]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                        else: # idk if this works
                            if leftfoot and R != 3:
                                if 3 not in nextlist and L != 3:
                                    next = [3]
                                elif L == 3:
                                    if 3 in next:
                                        next.remove(3)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            elif not leftfoot and L != 0:
                                if 0 not in nextlist and R != 0:
                                    next = [0]
                                elif R == 0:
                                    if 0 in next:
                                        next.remove(0)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                                else:
                                    tmpft = [x for x in range(1,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else:
                                if leftfoot: # 0,1,2
                                    if R == 0: # go back to last arrow
                                        if L not in nextlist:
                                            next = [L]
                                        else:
                                            tmpft = [x for x in range(0,4) if x not in nextlist]
                                            next = [choice(tmpft)]
                                    else:
                                        if 3 in next:
                                            next.remove(3)
                                        if L in next:
                                            next.remove(L)
                                        if R in next:
                                            next.remove(R)
                                else: # 1,2,3
                                    if L == 3:  # go back to last arrow
                                        if R not in nextlist:
                                            next = [R]
                                        else:
                                            tmpft = [x for x in range(0,4) if x not in nextlist]
                                            next = [choice(tmpft)]
                                    else:
                                        if 0 in next:
                                            next.remove(0)
                                        if L in next:
                                            next.remove(L)
                                        if R in next:
                                            next.remove(R)
                    elif p == 'spins': # not necessarily a spin but
                        if leftfoot and R == 0:
                            if L == 2:
                                next = [1]
                            elif L == 1:
                                next = [2]
                            else:
                                tmpft = [x for x in range(0,4) if x not in nextlist]
                                next = [choice(tmpft)]
                        elif not leftfoot and L == 3:
                            if R == 2:
                                next = [1]
                            elif R == 1:
                                next = [2]
                            else:
                                tmpft = [x for x in range(0,4) if x not in nextlist]
                                next = [choice(tmpft)]
                        elif leftfoot: # 0,1,2
                            if R == 0: # go back to last arrow
                                if L not in nextlist:
                                    next = [L]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else:
                                if 3 in next:
                                    next.remove(3)
                                if L in next:
                                    next.remove(L)
                                if R in next:
                                    next.remove(R)
                        else: # 1,2,3
                            if L == 3:  # go back to last arrow
                                if R not in nextlist:
                                    next = [R]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else:
                                if 0 in next:
                                    next.remove(0)
                                if L in next:
                                    next.remove(L)
                                if R in next:
                                    next.remove(R)
                    elif p == 'footswitches':
                        if L == 3 and R == 0:
                            if leftfoot: # 0,1,2
                                if Lsafe not in nextlist:
                                    next = [Lsafe]
                                else: # this applies for jumps so i need to stop changing it
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                            else: # 1,2,3
                                if Rsafe not in nextlist:
                                    next = [Rsafe]
                                else:
                                    tmpft = [x for x in range(0,4) if x not in nextlist]
                                    next = [choice(tmpft)]
                        elif leftfoot:
                            if R == 2 or R == 1:
                                if R not in nextlist:
                                    next = [R]
                                else:
                                    tmpft = [x for x in range(0,4) if x != R]
                                    next = [choice(tmpft)]
                            else:
                                if R == 0: # go back to last arrow
                                    if L not in nextlist:
                                        next = [L]
                                    else:
                                        tmpft = [x for x in range(0,4) if x not in nextlist]
                                        next = [choice(tmpft)]
                                else:
                                    if 3 in next:
                                        next.remove(3)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                        else:
                            if L == 2 or L == 1:
                                if L not in nextlist:
                                    next = [R]
                                else:
                                    tmpft = [x for x in range(0,4) if x != R]
                                    next = [choice(tmpft)]
                            else:
                                if L == 3:  # go back to last arrow
                                    if R not in nextlist:
                                        next = [R]
                                    else:
                                        tmpft = [x for x in range(0,4) if x not in nextlist]
                                        next = [choice(tmpft)]
                                else:
                                    if 0 in next:
                                        next.remove(0)
                                    if L in next:
                                        next.remove(L)
                                    if R in next:
                                        next.remove(R)
                    elif p == 'jacks':
                        if leftfoot: # do left again
                            next = [R]
                        else: # right again
                            next = [L]
                    elif p == 'repeats':
                        if leftfoot: # do last left
                            next = [L]
                        else: # last right
                            next = [R]
                    n = 0
                    if len(next) > 1:
                        n = randint(0,len(next)-1)
                nextlist.append(next[n])
                if leftfoot:
                    if next[n] == R and (R == 0 or R == 3) and not random: # prints debug info because this should never happen
                        print("Sideways footswitch warning: ", a, b, p, lastp, next, n, L, R)
                    if L != 3 and L != 0:
                        Lsafe = L
                    if str(next[n]) in lastset:
                        count += 1                       
                    Llast2 = Llast
                    Llast = L
                    L = next[n]
                    last = next[n]
                else:
                    if next[n] == L and (L == 0 or L == 3) and not random: # prints debug info because this should never happen
                        print("Sideways footswitch warning: ", a, b, p, lastp, next, n, L, R)
                    if R != 0 and R != 3:
                        Rsafe = R
                    if str(next[n]) in lastset:
                        count += 1
                    R = next[n]
                    last = next[n]
                leftfoot = not leftfoot
            for e in range(note[a][b].count('2')): # holds
                if nextlist[e] in fullholdlist:
                    tmphold = [x for x in range(0,4) if x not in nextlist]
                    nextlist[e] = choice(tmphold)
                holdlist.append(nextlist[e])
                fullholdlist.append(nextlist[e])
            if note[a][b].count('4'):
                for f in range(note[a][b].count('2'),note[a][b].count('4')): # rolls (note that holds are first and then rolls follow)
                    if nextlist[f] not in holdlist: # if there already isn't a hold there (failsafe)
                        rolllist.append(nextlist[f])
                        fullholdlist.append(nextlist[e])
            for g in range(note[a][b].count('3')): # hold ends
                endlist.append(fullholdlist[0])
                fullholdlist.remove(fullholdlist[0])
            mines = [i for i, x in enumerate(note[a][b]) if x == 'M'] # since it's a string idk if it will work
            for m in mines:
                minelist.append(m)
            nextset = num_to_arr(nextlist, holdlist, endlist, minelist, rolllist, fullholdlist)
            lastset = nextset
            temp.append(nextset) # note that it needs to be converted to the correct array
            if len(nextlist+holdlist+minelist+rolllist):
                leftfoot = not realleftfoot # multiple arrows it won't screw up step order
            lastmove = b
        new.append(temp)
    return new

def num_to_arr(nextlist, holdlist, endlist, minelist, rolllist, fullholdlist):
    array = [0,0,0,0,0]
    for i in nextlist:
        array[i] = 1
    for j in holdlist:
        array[j] = 2
    for r in rolllist:
        array[r] = 4
    for m in minelist: # if for some reason all spots are filled nothing will happen (shouldn't ever happen but in case)
        if len(nextlist+holdlist+rolllist):
            for i in nextlist+holdlist+rolllist:
                if m == i:
                    if array.count(0):
                        zeroes = [i for i, x in enumerate(array) if x == 0]
                        array[choice(zeroes)] = "M"
        else:
            array[m] = "M"
    for k in endlist:
        if len(nextlist+fullholdlist+rolllist+minelist):
            for i in nextlist+fullholdlist+rolllist+minelist:
                if k == i:
                    if overwrite_with_hold_ends:
                        array[k] = 3
                    else:
                        if not array.count(0): # if it can't do anything it will overwrite
                            array[k] = 3
                        else:
                            zeroes = [i for i, x in enumerate(array) if x == 0]
                            value = choice(zeroes)
                            for i in range(len(fullholdlist)):
                                if array[k] == fullholdlist[i]:
                                    fullholdlist[i] = array[value]
                            array[value] = array[k]
                            array[k] = 3
            array[k] = 3
        else:
            array[k] = 3
    #if len(endlist): print(array)
    return ''.join(str(e) for e in array)