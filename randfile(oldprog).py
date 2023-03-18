#Imports
import argparse
import os
from os import startfile
import numpy as np
import time
import sys

#Add command line arguments.
parser = argparse.ArgumentParser() #Initialize parser.
parser.add_argument('path', action="store", help='Path to folder.') #Add folder path.
parser.add_argument('-s', action='store_true', default=False, help='Optional: Include files in subdirectories?')
parser.add_argument('-c', action='store', dest='count', help='Optional: File count to open (default 1).')
parser.add_argument('-d', action='store', dest='delay', help='Optional: Delay N seconds between file opens (default 10).')
parser.add_argument('-i', action='store', dest='writefile', help='Optional: Save query as an index to Indexes folder with specified filename, rather than executing.')
parser.add_argument('-r', action='store', dest='readfile', help='Optional: Read from stored index with specified filename.')
parser.add_argument('-l','--list', dest='filetypes', nargs='+', type=str, help='Optional: List of filetypes to open.', required=False)
args = parser.parse_args() #Get arguments from command line.

#Get the path to the folder we're displaying from.
PATH = args.path

#Filetypes to open.
if (args.filetypes):
    fileTypes = args.filetypes;
else:
    fileTypes = ['jpg', 'png', 'jpeg', 'gif', 'move', 'mp4', 'mkv', 'webm']

#Function for recusrively fetching all files, including those in subdirectories.
def fetchAllFiles(path):
    items = os.listdir(path) #Get list of items in directory.
    files = [f for f in items if os.path.isfile(f'{path}/{f}') and f.split('.')[len(f.split('.')) - 1] in fileTypes] #Filter only files.
    files = [f'{path}/{f}' for f in files] #Add path to found filenames.
    directories = [d for d in items if os.path.isdir(f'{path}/{d}')] #Filter only directories.
    #Loop through all subdirectories.
    for d in directories:
        files.extend(fetchAllFiles(f'{path}/{d}')) #Recurse and combine with found files.
    return files #Return files.

#If read flag enabled, read from specified file, otherwise do normal indexing.
if args.readfile:
    file = open(f'./Indexes/{args.readfile}.txt', 'rb')
    files = file.read().decode('utf8')
    files = files.split('\n')
    files = [f for f in files if f.split('.')[len(f.split('.')) - 1] in fileTypes]
    file.close()
else:
    #If subdirectories flag enabled check recursively, otherwise just return files in specified dir.
    if args.s:
        files = fetchAllFiles(PATH)
    else:
        items = os.listdir(PATH)
        files = [f for f in items if os.path.isfile(f'{PATH}/{f}') and f.split('.')[len(f.split('.')) - 1] in fileTypes] #Filter only files.
        files = [f'{PATH}/{f}' for f in files] #Add path to found filenames.

#If no files found, error.
if len(files) == 0:
    print(f'No files found at {PATH}.')
    exit()

#Define how many files to open and with what delay.
delay = 10
count = 1
if args.count and int(args.count) > 0:
    count = int(args.count)
if args.delay and int(args.delay) > 0:
    delay = int(args.delay)

#If in index mode, write to file, otherwise do normal open sequence.
if args.writefile:
    file = open(f'./Indexes/{args.writefile}.txt', 'wb+')
    file.write('\n'.join(files).encode('utf8'))
    file.close()
else:
    for x in range(count):
        #Pick random file.
        fileName = np.random.choice(files)
        #if args.readfile:
        #    fileName = fileName.decode('utf8')[:-1]
        #Print filename and open file.
        print(fileName)
        startfile(f'{fileName}')
        #Wait before opening next file.
        if args.count or args.delay:
            time.sleep(delay)
exit()