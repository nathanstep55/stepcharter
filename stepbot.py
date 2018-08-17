# -*- coding: utf-8 -*-

'''
    StepBot, by Nathan Stephenson.
    
    StepBot is a Python 2/3 program that will automatically generate stepchart patterns for your StepMania charts based on existing rhythm.
    This program ensures that your steps won't be repetitive, while maintaining the correct rhythm and cues in a song that full chart generators often miss.
    
    Compatible with .sm files (and maybe .ssc files?), although I cannot guarantee that anything outside the 0,1,2,3,M spec will survive.
    Also supports only one difficulty at the moment, but I will work on fixing that.
    
    Pump stepcharts are also planned, for 6-panel and 9-panel not sure because I have no clue how the patterns work in those games.
'''

from __future__ import print_function
from builtins import input
from io import open

try: # Python 2
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError: # Python 3
    from tkinter import *
    from tkinter import filedialog

# ~~~~~ Configure these variables! ~~~~~
gamemode = "dance_single" # the only gamemode right now, will default if unknown
crossovers = True
crossovers_one_foot_at_a_time = True # prevents afronova walk etc.
crossover_between_measures = False
spins = False
footswitches = False
random = False

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