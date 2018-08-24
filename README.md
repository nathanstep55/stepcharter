# StepBot
by Nathan Stephenson

StepBot is a Python 2/3 program that will automatically generate stepchart patterns for your StepMania charts based on existing rhythm.
This program ensures that your steps won't be repetitive, while maintaining the correct rhythm and cues in a song that full chart generators often miss.

Compatible with .ssc and .sm files, however only the 0,1,2,3,4,M notes will survive at the moment (this will be fixed soon).
Also supports only one difficulty at the moment, but I will work on fixing that.

Pump stepcharts are also planned, for 6-panel and 9-panel not sure because I have no clue how the patterns work in those games.
Once I have implemented multiple gamemodes you will be able to convert existing charts into the gamemode of your choice.

Command line support has been added and works as such:
```
python stepbot.py -i <input file> -o <output file>
```
If you are missing any it will prompt you (the original way to get files).