import time
import os
import re
import math
import keyboard
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def ClearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

startingTimeStamp = ""
endingTimeStamp = ""

#Regex for HH:MM:SS
timePattern = re.compile(r"\d{2}:\d{2}:\d{2}")

runs = []
realRuns = {}

def RunIndex():
    RunIndex.counter += 1
    return RunIndex.counter

RunIndex.counter = 0

#a snippet that I grabbed from stackoverflow, need to figure out an asyncronous way to handle this
def Follow(thefile):
    thefile.seek(0,os.SEEK_END) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        return line

def CheckLog(thefile,endOfFile):
    curEnd = thefile.seek(0,os.SEEK_END)
    if endOfFile != curEnd:

        thefile.seek(0,os.SEEK_END)

# Returns the difference between two datetime objects in seconds
def TimeDifferenceInSeconds(timeStamp1, timeStamp2):
    FMT = "%H:%M:%S"
    timeDelta = datetime.strptime(timeStamp2, FMT) - datetime.strptime(timeStamp1, FMT)
    return timeDelta.seconds
    
#Prints the run with the information given
def PrintRun(timeStarted, seconds):

    #Record the run
    runs.append(seconds)
    realRuns[str(timeStarted)] = seconds

    #Build the string to print
    timeStringText = ""
    timeStringText = "Run No: " + str(RunIndex()) + " | "
    timeStringText = timeStringText + str(seconds) + " second(s)\t"

    #The definition of pointless
    runCount = len(runs)
    if runCount == 0:
        print("Let's not divide by zero, k?")
        return

    averageTime = sum(runs)/len(runs)
    timeStringText= timeStringText + " | Average time: " + str(round(averageTime,3)) + " seconds."

    #We got this far, print!
    print(timeStringText)
    return

def WatchLog(RunActive, logFile):
  
    while True:

        where = logFile.tell
        line = Follow(logFile)

        #ClearConsole()
        #print(keyboard._pressed_events)

        if not line:
            logFile.seek(where)

        else:
            if line.__contains__("You have entered "):
                if line.__contains__("Ossuary") or line.__contains__("Blood"): #yeah I was recording blood aquaduct times, shoot me
                    if not RunActive:

                        RunActive = True
                        startingTimeStamp = timePattern.search(line).group(0)

                elif RunActive:

                    RunActive = False
                    endingTimeStamp = timePattern.search(line).group(0)
                    runTimeInSeconds = TimeDifferenceInSeconds(startingTimeStamp, endingTimeStamp)
                    PrintRun(startingTimeStamp, runTimeInSeconds)
            
            #potential place to exit while for keyboard input
        

def main():

    #Initializing shit
    root = tk.Tk()
    root.withdraw()

    #ask for the client.txt location, and open it
    logFileName = filedialog.askopenfilename()
    logFile = open(logFileName,'r')

    runStarted = False
    stopped = False
    ClearConsole()
    while not stopped:
        WatchLog(runStarted, logFile)
        #if keyboard.is_pressed(keyboard._pressed_events['q']):
        #    stopped = True
    #print(keyboard._pressed_events)

if __name__ == "__main__":
    main()