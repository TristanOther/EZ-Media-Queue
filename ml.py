###########
# Imports #
###########
import PySimpleGUI as gui
import os
import numpy as np

####################
# Global Variables #
####################
PATH = '' # Constant for storing user-inputted path.
SUB = True # Whether or not we're parsing subdirectories (user defined).
INDEX = [] # List of all indexed filepaths.
FILTERED_INDEX = [] # List of indexed filepaths filtered (filetypes, subdirectories, etc.)
HISTORY = [] # History of opened files.
CUR_FILE = 0 # Index of current file in history.
FILE_TYPES = [] # Whitelisted filetypes (user defined).
USE_FILE_TYPES = False # Whether or not to use custom file types.
SPECS_CHANGED = True # Track when a specification is changed so FILTERED_INDEX can be updated on next file request.

#############
# Build GUI #
#############
gui.theme('Black')
# Path selection row.
pathRow = [
    gui.Text('Folder Path:'),
    gui.In(size=(50,1), enable_events=True, key='path_sel'),
    gui.FolderBrowse(),
    gui.Checkbox('Include Subdirectories', default=True, enable_events=True,  key='read_sub')
]
# Filetypes row.
fileTypeRow = [
    [gui.Text('Filetypes (seperated by spaces):', pad=(0, 20)),
    gui.InputText(pad=(10, 20), enable_events=True, key='filetypes'),
    gui.Checkbox('Custom Filetypes', default=False, pad=(0, 20), enable_events=True, key='filter_filetypes')]
]
# Control button row.
ctrlBttnRow = [
    gui.Button('Previous', font=('Arial Bold', 20), size=(8, 1), key='prev'),
    gui.Button('Next', font=('Arial Bold', 20), size=(8, 1), key='next')
]
# Assemble layout.
layout = [
    pathRow,
    fileTypeRow,
    ctrlBttnRow,
    [gui.Text('Current File:'), gui.Text('', key='cur_file_text')],
    [gui.Button('debug', key='debug', visible=False)]
]
# Create the window.
window = gui.Window('EZ Media Queue', layout)

####################
# Helper Functions #
####################
# Function for indexing a path.
def indexPath(path):
    global PATH
    PATH = path
    handleFiles()

# Function for handling events received by our window.
def handleEvents(event, values):
    global USE_FILE_TYPES
    global FILE_TYPES
    global SUB
    global SPECS_CHANGED
    file = None
    if event in (gui.WIN_CLOSED, 'Cancel'):
        window.close()
        exit()
    elif event == 'debug':
        print(f'Path:{PATH}\nSub:{SUB}\nIndex Size:{len(INDEX)}\nHistory:{HISTORY}\nFile Index:{CUR_FILE}\nFile Types:{FILE_TYPES}\nUse Filetypes:{USE_FILE_TYPES}\n')
    elif event == 'path_sel':
        indexPath(values['path_sel'])
        SPECS_CHANGED = True
    elif event == 'read_sub':
        SUB = values['read_sub']
        SPECS_CHANGED = True
    elif event == 'prev':
        file = prevItem()
    elif event == 'next':
        file = nextItem()
    elif event == 'filetypes' or event == 'filter_filetypes':
        FILE_TYPES = values["filetypes"].split(" ")
        USE_FILE_TYPES = values['filter_filetypes']
        SPECS_CHANGED = True
    if file:
        os.startfile(file)
    return

# Function for getting the previous item in the history.
def prevItem():
    global CUR_FILE
    # Return if we're at the beginning of the history.
    if CUR_FILE == 0:
        return
    # Return the previous file in our history list.
    CUR_FILE -= 1
    return HISTORY[CUR_FILE]

# Function for getting the next item in the queue.
def randomItem():
    global HISTORY
    global SPECS_CHANGED
    if SPECS_CHANGED:
        reindex()
        SPECS_CHANGED = False
    file = np.random.choice(FILTERED_INDEX)
    HISTORY.append(file)
    return file

# Function for getting a random item in the queue.
def nextItem():
    global CUR_FILE
    # If we're not currently looking at a file in the history, get a new random file.
    if not HISTORY or CUR_FILE == len(HISTORY) - 1:
        CUR_FILE += 1
        return randomItem()
    # If we're looking at a file in the history, advance to the next most recent file in the history.
    CUR_FILE += 1
    return HISTORY[CUR_FILE]

########################
#File Fetching Functions
########################
# Function for filtering all indexed files with current specifications.
def reindex():
    global FILTERED_INDEX
    if USE_FILE_TYPES:
        fileTypes = FILE_TYPES
    else:
        fileTypes = ['mp3', 'mp4', 'mov', 'mkv', 'png', 'jpg', 'jpeg', 'gif', 'webm', 'txt', 'pdf']
    files = [f for f in INDEX if os.path.isfile(f) and f.split('.')[len(f.split('.'))-1] in fileTypes]
    if not SUB:
        files = [f for f in files if (f == f'{PATH}/{f.split("/")[-1]}')]
    FILTERED_INDEX = files
    
#Fetch all files in directory.
def fetchFiles(items, path):
    # Filter only files in pathed directory and prepend the path to the filename.
    files = [f'{path}/{f}' for f in items if os.path.isfile(f'{path}/{f}')] 
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
    global INDEX
    files = fetchAllFiles(PATH)
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
    handleEvents(event, values)
    if HISTORY:
        window['cur_file_text'].update(HISTORY[CUR_FILE])
