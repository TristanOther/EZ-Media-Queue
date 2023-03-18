###########
# Imports #
###########
import PySimpleGUI as gui
import os
import numpy as np
import time

####################
# Global Variables #
####################
PATH = '' # Path to our folder
SUB = True # Whether or not we're parsing subdirectories.
INDEX = [] # Indexed files
HISTORY = [] # Opened file history.
FUTURE = [] # History of opened files we've gone back from.
FILE_TYPES = [] # Whitelisted filetypes.
USE_FILE_TYPE = False # Whether or not to use custom file types.

#############
# Build GUI #
#############
gui.theme('Black')
# Path selection row.
pathRow = [
    gui.Text('Folder Path:'),
    gui.In(size=(50,1), enable_events=True, key='path_sel'), 
    gui.FolderBrowse(),
    gui.Checkbox('Include Subdirectories', default=True, key='read_sub')
]
# Filetypes row.
fileTypeRow = [
    [gui.Text('Filetypes (comma seperated):', pad=(0, 20)),
    gui.InputText(pad=(10, 20), key='filetypes'), 
    gui.Checkbox('Custom Filetypes', default=False, pad=(0, 20), key='filter_filetypes')]
]
# Control button row.
ctrlBttnRow = [
    gui.Button('Previous', font=('Arial Bold', 20), size=(8, 1), key='prev'),
    gui.Button('Random', font=('Arial Bold', 20), size=(8, 1), pad=(20, 0),  key='rand'),
    gui.Button('Next', font=('Arial Bold', 20), size=(8, 1), key='next')
]
# File history row.
histRow = [
    [gui.Text('History:')],
    gui.Text('TEST TEXT...', key='history_text')
]
# Assemble layout.
layout = [
    pathRow,
    fileTypeRow,
    ctrlBttnRow,
    [gui.Button('debug', key='debug')]
]
# Create the window.
window = gui.Window('EZ Media Queue', layout)

####################
# Helper Functions #
####################
# Function for indexing a path.
def indexPath(path):
    global PATH
    if path == PATH:
        return
    PATH = path
    handleFiles()
    print('Index updated.')

# Function for handling a button event.
def processButton(event):
    if event == 'rand':
        file = randomItem()
    elif event == 'prev':
        file = prevItem()
    elif event == 'next':
        file = nextItem()
    else:
        return
    if file:
        os.startfile(file)

# Function for getting the previous item in the history.
def prevItem():
    global HISTORY
    global FUTURE
    if len(HISTORY) < 2:
        return
    FUTURE.insert(0, HISTORY.pop(-1))
    return HISTORY[-1]

# Function for getting the next item in the queue.
def randomItem():
    global INDEX
    global HISTORY
    file = np.random.choice(INDEX)
    HISTORY.append(file)
    return file

# Function for getting a random item in the queue.
def nextItem():
    global HISTORY
    global FUTURE
    # TODO: add functionality for getting a logical next item instead of this condition
    if len(FUTURE) == 0:
        return
    HISTORY.append(FUTURE.pop(0))
    return HISTORY[-1]

########################
#File Fetching Functions
########################
#Fetch all files in directory.
def fetchFiles(items, path):
    global FILE_TYPES
    global USE_FILE_TYPE
    if USE_FILE_TYPE:
        fileTypes = FILE_TYPES
    else:
        fileTypes = ['mp3', 'mp4', 'mov', 'mkv', 'png', 'jpg', 'jpeg', 'gif', 'webm', 'txt', 'pdf']
    files = [f for f in items if os.path.isfile(f'{path}/{f}') and f.split('.')[len(f.split('.'))-1] in fileTypes] #Filter only files in pathed directory.
    files = [f'{path}/{f}' for f in files] #Add path to found filenames.
    return files

#Recusively fetch all files in a directory and its subdirectories.
def fetchAllFiles(path):
    items = os.listdir(path)
    files = fetchFiles(items, path)
    directories = [d for d in items if os.path.isdir(f'{path}/{d}')]
    for d in directories:
        p = f'{path}/{d}'
        files.extend(fetchAllFiles(p))
    return files

#Function for handling whether or not to fetch files in subdirectories or just the files in the provided directory.
def handleFiles():
    global PATH
    global INDEX
    if SUB:
        files = fetchAllFiles(PATH)
    else:
        files = fetchFiles(os.listdir(PATH), PATH)
    #If no files found, error.
    if len(files) == 0:
        print(f'No files found at {PATH}.')
        exit()
    INDEX = files

##############
# Event Loop #
##############
while True:
    event, values = window.read()
    if event in (gui.WIN_CLOSED, 'Cancel'):
        break
    elif event == 'debug':
        print(f'Path:{PATH}\nSub:{SUB}\nIndex Size:{len(INDEX)}\nHistory:{HISTORY}\nFuture:{FUTURE}\nFile Types:{FILE_TYPES}\nUse Filetypes:{USE_FILE_TYPE}\n')
    elif event == 'path_sel':
        indexPath(values['path_sel'])
    else:
        processButton(event)
    #window['history_text'].update(str(values))
window.close()

# TODO:
# Tracker for previous 10 items displayed]
# Current item displayed
# Next item displayed
# Add event and function for updating filetypes
# Fix subdirectories
# Implement Next button