# -*- coding: utf-8 -*-

'''
    StepBot, by Nathan Stephenson.
    
    StepBot is a Python 2/3 program that will automatically generate stepchart patterns for your StepMania charts based on existing rhythm.
    This program ensures that your steps won't be repetitive, while maintaining the correct rhythm and cues in a song that full chart generators often miss.
    
    Compatible with .sm files (and maybe .ssc files?), although I cannot guarantee that anything outside the 0,1,2,3,M spec will survive.
    Also supports only one difficulty at the moment, but I will work on fixing that.
    
    Pump stepcharts are also planned, for 6-panel and 9-panel not sure because I have no clue how the patterns work in those games.
'''

# stuff to make compatible with Python 3
from __future__ import print_function
from builtins import input
from io import open

from random import randint, choice
import sys

try: # Python 2
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError: # Python 3
    from tkinter import *
    from tkinter import filedialog

# ~~~~~ Configure these settings! ~~~~~
gamemode = "dance_single" # the only gamemode right now, will default if unknown
crossover_between_measures = False # false to make an attempt at less awkward patterns
random = False

# Weights: Configure how often you want certain patterns to occur as a decimal
crossovers = 0.1
spins = 0.05 # this doesn't necessarily mean a full spin
footswitches = 0.05
jacks = 0.1
repeats = 0.35 # drills, triples, etc.
#symmetrical_patterns - to be implemented

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

normal = 1 - crossovers - spins - footswitches - repeats

if normal > 1 or normal < 0:
    sys.exit("Error: Your weights are invalid. Please make sure that they all add up to a number in between 0 and 1.")

def get_notes(sim): # modified from jmania and is simpler because python is wayyy better
    note = []
    for i in range(len(sim)):
        if "#NOTES:" in sim[i]: # to make multiple difficulties you would have to check for the next difficulty and replace len(sim) in the next for loop
            notestr = ""
            for a in range(i+1,len(sim)):
                if "     " not in sim[a]:
                    notestr += sim[a].replace(";", "").replace('\n', '')
            noteslist = notestr.split(",")
            for b in range(len(noteslist)):
                n = get_gm_num(gamemode)
                note.append([noteslist[b][i:i+n] for i in range(0, len(noteslist[b]), n)]) # splits every n arrows into separate strings
            return note
    return note
    
def get_gm_num(gm): # how many arrows per gamemode
    gms = {
        "dance_single": 4,
        "pump_single": 5,
        "solo": 6,
        "dance_double": 8, 
        "technomotion": 9,
        "pump_double": 10
    }
    if gms[gm]:
        return gms[gm]
    else:
        return 4

def generate(note):
    new = []
    leftfoot = bool(randint(0,1))
    lastnote = [0,0,0,0]
    for a in range(len(note)):
        temp = []
        for b in range(len(note[a])):
            next = [0,1,2,3]
            if note[a][b] = [0,0,0,0]:
                continue
            if 2 in note[a][b]:
                holds = [i for i, x in enumerate(note[a][b]) if x == 2]
            if random:
                n = randint(0,3)
            else:
                patterns = ['normal']*(100*normal) + ['crossovers']*(100*crossovers) + ['spins']*(100*spins) + ['footswitches']*(100*footswitches) + ['jacks']*(100*jacks) + ['repeats']*(100*repeats)
                p = choice(patterns)
                n = 0
                if len(next) > 1:
                    n = randint(0,len(next)-1)
            if lastnote.count(1) + lastnote.count(2) > 1:
                # this only handles one note i need to handle two notes
                # probably random generation whether foot switches or not
            temp.append() # note that it needs to be converted to the correct array
            lastnote = next
            leftfoot = not leftfoot
        new.append(temp)
        
root = Tk()
root.withdraw()
path = filedialog.askopenfilename()

f = open(path, 'rt')
print("File opened.")

simlines = f.readlines()

notes = get_notes(simlines) # convert notes split into arrays of measures split into arrays of beats
print(notes)

newchart = generate(notes)

# We're going to have to keep track of two different arrays:
# - old notes to keep track of holds
# - new notes for new simfile

# Possibilities can be calculated either in a dictionary or with this code:
# next = [0,1,2,3]
# if random
#   p = random
# else
#   patterns = ['normal']*(100*normal) + ['crossovers']*(100*crossovers) + ['spins']*(100*spins) + ['footswitches']*(100*footswitches) + ['jacks']*(100*jacks) + ['repeats']*(100*repeats)
#   p = choice(patterns)
# - if random
#   - randint(0,3)
# - if normal
#   - if leftfoot:
#     - next.remove(L)
#     - next.remove(R)
#     - next.remove(3)
#   - else:
#     - next.remove(L)
#     - next.remove(R)
#     - next.remove(0)
# - if footswitches
#   - remove all but previous arrow on last foot if 1 or 2
#   - also no crossover should happen (L cannot be 3, R cannot be 0)
# - if jacks
#   - remove all but previous arrow on last foot
#   - DO NOT CHANGE FOOT
# - if crossovers
#   - if L is 3 and R was 1 or 2
#     - if spins
#       - whatever
#     - if not spins
#       - R is 1 or 2 again
# - if repeats
# - if more than one note left
#   - randint(len(next))