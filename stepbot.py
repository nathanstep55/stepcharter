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
crossovers_one_foot_at_a_time = True # prevents afronova walk etc.
crossover_between_measures = False # false to make an attempt at less awkward patterns
random = False

# Weights: Configure how often you want certain patterns to occur as a decimal
crossovers = 0.1
spins = 0.05
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
    
root = Tk()
root.withdraw()
path = filedialog.askopenfilename()

f = open(path, 'rt')
print("File opened.")

simlines = f.readlines()

notes = get_notes(simlines) # convert notes split into arrays of measures split into arrays of beats
print(notes)

# We're going to have to keep track of two different arrays:
# - old notes to keep track of holds
# - new notes for new simfile

# Possibilities can be calculated either in a dictionary or with this code:
# next = [0,1,2,3]
# if random
#   p = random
# else
#   patterns = ['normal']*normal + ['crossovers']*crossovers + ['spins']*spins + ['footswitches']*footswitches + ['jacks']*jacks + ['repeats']*repeats
#   p = choice(patterns)
# - if random
#   - randint(0,3)
# - if footswitches
#   - L and R positions should not be right after each other if 0 or 3
#   - also no crossover should happen (L cannot be 3, R cannot be 0)
# - if not footswitches
#   - L and R positions should never be right after each other
# - if crossovers
#   - if L is 3 and R was 1 or 2
#     - if spins
#       - whatever
#     - if not spins
#       - R is 1 or 2 again
# - if not crossovers
#   - L should not be 3 and R should not be 0
# - if more than one note left
#   - randint(len(next))