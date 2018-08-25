#Stepcharter
by Nathan Stephenson

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