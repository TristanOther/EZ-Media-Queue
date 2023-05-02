## Welcome to EZ Media Queue!
Do you have a large library of photos, videos, music, or other media, but never know what to watch? EZ Media Queue is the solution to this incredibly random problem! With this program you can view any and all media on your computer with the press of a button. This program opens the specified media using whatever program you have set as default in Windows, so your favorite settings and features are all availible for any media you wish to browse. To begin, follow the usage instructions below!

## How to use:
### Installation:
To use this project, simply download the ml.py file from this repository and run it using Python. This project currently requires Python 3 and the PySimpleGUI library are installed to use. When run, the program will open its GUI, and is ready to use.

![Image highlighting GUI elements so they can be explained below.](https://github.com/TristanOther/EZ-Media-Queue/blob/main/Misc/Images/example.png)
The above image highlights the important UI sections of this application. Below I'll explain each section and what it does.

### Path Selector (Highlighted Red):
Here we see 2 input sections, a textbox and a checkbox. The textbox is where the path to the folder you wish to browse should be entered. You can enter the path in manually, or hit the browse button to navigate to the path using the Windows file selector. Only media at this path will be viewed by the program. 

Next to the path selector is a checkbox labled "Include Subdirectories". This box is checked by default. When checked, the program will include media in all folders within the folder you specify with the path selector. If you choose to unselect this, any media stored in subfolders will not be played.

### Filetype Input (Highlighted Yellow):
Again we see 2 input sections, a textbox and a checkbox. In the textbox you can enter filetypes you want the program to browse, seperated by spaces. In our example image we have png, jpg, gif, and mp4 files specified, but you can specify any filetypes you want. The default if no filetypes are specified is mp3, mp4, mov, mkv, png, jpg, jpeg, gif, webm, txt, and pdf.

Next to the filetypes input box there is a checkbox labeled "Custom Filetypes". When left unchecked, any filetypes in the input box will be used. In order to filter by filetypes you must check this box.

### Navigation Buttons (Highlighted Green):
Here we see 2 buttons. The first button, labled "Previous", behaves as you might expect. When browsing media if you skip past a file you want to go back to you can hit the "Previous" button to go back through the entire history of opened files. 

The "Next" button is a bit more complicated. When this button is pressed a random piece of media at the location and with the filters specified in previous steps will be opened. However, if you've hit the previous button and are currently browsing history this will advance through the media you went back through until you're back at the start. Basically, if the "Previous" button takes you backwards in the opened file history, the "Next" button will take you forwards if applicable. 

NOTE: When the "Next" button is pressed after any settings have been changed it may take a minute to open a file, as files need to be reparsed with new settings.

### Current File (Highlighted Blue):
This section simply displays the path (with filename) of the most recently opened file. If you want to know exactly where the file is located (only really applicable with the "Include Subdirectories" option enabled) this may be useful.

## Licensing:
MIT License

Copyright (c) 2023 https://github.com/TristanOther

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
  
2. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

Why you'd want to copy this I have no idea, but I figure I'll give you permission anyway ;)

