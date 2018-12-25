# -*- coding: utf-8 -*-

'''
    Stepcharter, by Nathan Stephenson.
    
    Stepcharter (originally StepBot) is a Python 2/3 program that will automatically generate stepchart patterns for your StepMania charts based on existing arrows.
    This program ensures that your steps won't be repetitive, while maintaining the correct rhythm and cues in a song that full chart generators often miss.
    You can use this to make charts more efficiently and also to convert charts between gamemodes.
    
    Compatible with .ssc and .sm files, however only the 0,1,2,3,4,M notes will survive at the moment (this will be fixed soon).
    Also supports only one difficulty at the moment, but I will work on fixing that.
    
    Stepcharter now supports converting ALL StepMania gamemodes to dance-single.
    It will automatically detect the current gamemode and switch it to dance-single, generating new arrows.

    As of now, dance-single is the only gamemode that can be generated, but support for all gamemodes is planned (including keyboard charts).
    If anyone can explain 6-panel and 9-panel patterns, feel free to send me a message.

    Command line support has been added and works as such:
    ```
    python stepcharter.py -i <input file> -o <output file>
    ```
    If you are missing any it will prompt you through Open/Save windows.
'''

# stuff to make compatible with Python 2 and 3
from __future__ import print_function
from builtins import input
from io import open

from importlib import import_module
from random import randint, choice
import sys, codecs, argparse

try: # Python 2
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError: # Python 3
    from tkinter import *
    from tkinter import filedialog

# ~~~~~ Configure these settings! ~~~~~
gamemode = "pump-single" # the only gamemode right now, will default if unknown
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

gms = {
    "dance-single": [4,"dancesingle"],
    "pump-single": [5,"pumpsingle"],
    "solo": [6,"solo"],
    "dance-double": [8,"dancedouble"], 
    "technomotion": [9,"technomotion"],
    "pump-double": [10,"pumpdouble"]
}

def get_notes(sim): # modified from jmania and is simpler because python is wayyy better
    note = []
    tempgm = ""
    for i in range(len(sim)):
        if "#STEPSTYPE:" in sim[i]: # probably only works with ssc
            tempgm = sim[i].replace("#STEPSTYPE:", "").replace(";", "").replace('\n', '').replace('\r', '')
        elif "#NOTES:" in sim[i]: # to make multiple difficulties you would have to check for the next difficulty and replace len(sim) in the next for loop
            notestr = ""
            for a in range(i+1,len(sim)):
                if "     " not in sim[a]:
                    notestr += sim[a].replace(";", "").replace('\n', '').replace('\r', '')
            noteslist = notestr.split(",")
            for b in range(len(noteslist)):
                n = get_gm_num(tempgm)
                note.append([noteslist[b][i:i+n] for i in range(0, len(noteslist[b]), n)]) # splits every n arrows into separate strings
            return note
    return note
    
def get_gm_num(gm): # how many arrows per gamemode
    try:
        return gms[gm][0]
    except:
        print("Could not determine gamemode, defaulting to 4 arrows")
        return 4

def export(sim, new, path):
    e = codecs.open(path, 'w', encoding='UTF-8')
    for i in range(len(sim)):
        for key in gms.keys():
            if key in sim[i]:
                sim[i] = sim[i].replace(key, gamemode)
        e.write(sim[i])
        if "#NOTES:" in sim[i]:
            for a in range(i+1,len(sim)):
                if "     " not in sim[a]:
                    break
                else:
                    e.write(sim[a])
            for b in range(len(new)):
                for c in range(len(new[b])):
                    e.write(new[b][c]+"\n")
                if b != len(new)-1:
                    e.write(",\n")
                else:
                    e.write(";\n")
            break
    e.close()

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-i', action="store", dest="input", help='The input simfile to modify')
    parser.add_argument('-o', action="store", dest="output", help='The output simfile to export')
    #parser.add_argument('--append', action='store_true', help='Add to existing simfile instead of replacing it')

    #parser.add_argument('-gm', action="store", dest="output", help='The gamemode to convert to (dance-single, pump-double, etc.)')

    args = parser.parse_args()

    if args.input == None or args.output == None:
        root = Tk()
        root.withdraw()

    if args.input != None:
        path = args.input
    else:
        path = filedialog.askopenfilename()
        if path == '':
            sys.exit("Canceled.")

    f = codecs.open(path, 'r', encoding='UTF-8')
    print("File opened.")

    try:
        gm_module = import_module(gms[gamemode][1])
    except: # default to dancesingle
        print("Could not find or execute code for specified gamemode, defaulting to dancesingle")
        gm_module = import_module("dancesingle")

    generate = getattr(gm_module, "generate")

    simlines = f.readlines()

    notes = get_notes(simlines) # convert notes split into arrays of measures split into arrays of beats
    #print(notes)

    seed = None # for now but make sure this becomes an argparse
    newchart = generate(notes, seed)

    if args.output != None:
        path2 = args.output
    else:
        path2 = filedialog.asksaveasfilename()
        if path2 == '':
            sys.exit("Canceled.")

    export(simlines, newchart, path2) # add append mode
    f.close()
    print("Exported as simfile " + path2)

if __name__ == "__main__":
    main()