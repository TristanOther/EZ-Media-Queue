########
#Imports
########
import argparse #Parser for command-line arguments.
import os
from os import startfile #Allows for files to be opened in their default app.
import numpy as np #Numpy, for math stuff. Used for random list selection here.
import time #Allows for sleep.

#######################
#Command-Line Arguments
#######################
parser = argparse.ArgumentParser() #Initialize parser.
parser.add_argument("path", action="store", help="Path to folder or index file.") #Argument for path to folder to be searched or index file to read/write.
parser.add_argument("-s","--subdirectories", action="store_true", dest="s", default=False, help="scan files in subdirectories [optional]", required=False) #Argument for toggle querying subdirectories.
parser.add_argument("-wi","--writeindex", action="store", dest="index_path", help="index items queried and store in a text file at given path [optional]", required=False) #Argument for indexing queried results.
parser.add_argument("-ri","--readindex", action="store_true", dest="ri", default=False, help="use index file to run query [optional]", required=False) #Argument for querying from indexed results.
parser.add_argument("-c","--count", action="store", dest="c", help="open C files with query [optional]", required=False) #Argument for how many files to open.
parser.add_argument("-d","--delay", action="store", dest="d", help="delay D seconds between file opens [optional]", required=False) #Argument for delay between opening files.
parser.add_argument("-ft","--filetypes", dest="filetypes", nargs="+", type=str, help="filetypes to limit query to [optional]", required=False) #Argument for query filetypes.
args = parser.parse_args() #Get arguments from command line.

###################################
#Initialize Argument Vars and Check
###################################
#Ensure read and write index not enabled at same time.
if args.ri and args.index_path:
    print("You can't read and write indexes in the same query.")
    exit()
#Ensure count is a positive integer.
count = 1
if args.c:
    if int(args.c) <= 0:
        print("Count must be a positive integer.")
        exit()
    count = int(args.c)
#Ensure delay is a positive integer or 0.
delay = 0
if args.d:
    if int(args.d) < 0:
        print("Delay must be a positive integer or 0.")
        exit()
    delay = int(args.d)
#Override default filetypes if necessary.
fileTypes = ["jpg", "jpeg", "png", "gif", "webm", "mp3", "mp4", "mov", "mkv", "txt"]
if args.filetypes:
    fileTypes = args.filetypes

########################
#File Fetching Functions
########################
#Fetch all files in directory.
def fetchFiles(items, path):
    files = [f for f in items if os.path.isfile(f"{path}/{f}") and f.split(".")[len(f.split("."))-1] in fileTypes] #Filter only files in pathed directory.
    files = [f'{path}/{f}' for f in files] #Add path to found filenames.
    return files
#Recusively fetch all files in a directory and its subdirectories.
def fetchAllFiles(path):
    items = os.listdir(path)
    files = fetchFiles(items, path)
    directories = [d for d in items if os.path.isdir(f"{path}/{d}")]
    for d in directories:
        p = f"{path}/{d}"
        files.extend(fetchAllFiles(p))
    return files
#Function for handling whether or not to fetch files in subdirectories or just the files in the provided directory.
def handleFiles(path):
    if args.s:
        files = fetchAllFiles(path)
    else:
        files = fetchFiles(os.listdir(path), path)
    #If no files found, error.
    if len(files) == 0:
        print(f"No files found at {PATH}.")
        exit()
    return files
#############
#Main Program
#############
#Function for opening files.
def openFiles(files):
    for x in range(count):
        fileName = np.random.choice(files)
        print(fileName)
        startfile(fileName)
        time.sleep(delay)
    exit()
#Handle if writing to index.
if args.index_path:
    files = handleFiles(args.path)
    file = open(args.index_path, "wb+")
    file.write("\n".join(files).encode("utf8"))
    file.close()
    exit()
#Handle if reading from index.
elif args.ri:
    file = open(args.path, "rb")
    files = file.read().decode("utf8")
    files = files.split("\n")
    files = [f for f in files if f.split(".")[len(f.split(".")) - 1] in fileTypes]
    file.close()
    openFiles(files)
#Handle if just opening a file normally.
else:
    files = handleFiles(args.path)
    openFiles(files)