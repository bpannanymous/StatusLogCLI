#===
#libraries
#===
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import os
from pathlib import Path
import GeneralFunctions
import Functions
import shutil

#===
#path to readings
#===
cpu_temp_path=Path("/sys/class/hwmon/hwmon5/temp1_input") #cpu temperature file
gpu_temp_path=Path("/sys/class/hwmon/hwmon6/temp1_input") #gpu temperature file
fan_speed_path=Path("/sys/class/hwmon/hwmon5/fan1_input") #fan speed file
power_path=Path("/sys/class/hwmon/hwmon3/power1_input") #power consumption file

#===
#initial menu
#===
choice=Functions.initialMenu()

#===
#main code
#===
while True: #iterate
    if choice=='R': #run test
        while True:
            frequency,measurements,FileName,decision,notes=Functions.createTest() #take initial parameters
            if FileName=='E' or decision=='N' or frequency=='E' or measurements=='E': #if they would not like to proceed
                break
            else: #if they would like to proceed
                FilePath='Logs/'+FileName #create path
                print('Creating File...') #output message to denote file creation
                time.sleep(1) #1 second delay
                with open(FilePath,"w") as file: #open new file as writeable
                    pass
                print(FileName,'successfully created') #success message
                time.sleep(0.5)
                print('Beginning Test')
                time.sleep(2)
                Functions.runTest(frequency,measurements,notes,FilePath,cpu_temp_path,gpu_temp_path,fan_speed_path,power_path) #run diagnostic with given parameters
                GeneralFunctions.Space(1)
                input('Test Complete. Preas ENTER to return to selection menu. ') #wait for user input to proceed
                break
        choice=Functions.initialMenu() #go back to start menu
    elif choice=='P': #plot test
        plotDecision=Functions.plotMenu()
        while True: #iterate
            if plotDecision=='C':
                Functions.plotTest('CPU Temperature Evolution','C','CPU Temperature (C)',30,100,1) #plot cpu temperature
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='G':
                Functions.plotTest('GPU Temperature Evolution','C','GPU Temperature (C)',30,100,2) #plot gpu temperature
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='F':
                Functions.plotTest('Fan Speed Evolution','rpm','Fan Speed (rpm)',0,6000,3) #plot fan speed
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='P':
                Functions.plotTest('Power Draw Evolution','W','Power Consumption (W)',0,35,4) #plots power consumption
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            else: #exit menu
                break
        choice=Functions.initialMenu() #go back to start menu
    elif choice=='O': #overlay test plots
        plotDecision=Functions.plotMenu() #ask what they would like to plot
        while True:
            if plotDecision=='C': #plot cpu temperature
                Functions.multiPlot('C','CPU Temperature (C)',30,100,1) #plot cpu temperature
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='G': #plot gpu temperature
                Functions.multiPlot('C','GPU Temperature (C)',30,100,2) #plot gpu temperature
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='F': #plot fan speed
                Functions.multiPlot('rpm','Fan Speed (rpm)',0,6000,3) #plot fan speed
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            elif plotDecision=='P': #plot power consumption
                Functions.multiPlot('W','Power Consumption (W)',0,35,4) #plots power consumption
                GeneralFunctions.clear()
                plotDecision=Functions.plotMenu() #reask for plot operation
            else: #exit menu
                break
        choice=Functions.initialMenu()
    elif choice=='V': #view test
        while True: #iterate until specified otherwise
            FilePath=Functions.selectTest() #specify test to view and return its filepath
            if FilePath=='Logs/E': #if they would like to exit loop
                break #break loop
            else: #if they actually entered a file
                with open(FilePath,"r") as file: #open file as readable
                    All=file.readlines() #read all lines and assign it to a list
                    GeneralFunctions.clear() #clear TUI
                    for i in range(len(All)):
                        currentLine=str(All[i]) #assign the current element to a variable
                        currentLine=currentLine[:-1] #remove the last character which is a new line operation
                        print(currentLine) #print the line
                    GeneralFunctions.Space(1)
                    GeneralFunctions.Line(30)
                    input('Press ENTER to return to previous screen. ') #return option
        choice=Functions.initialMenu() #go back to start menu
    elif choice=='L': #list tests
        GeneralFunctions.ListFiles('Logs','Previous Tests') #list files in Logs directory
        input('Press ENTER to return to previous menu') #wait for input to advance
        GeneralFunctions.clear() #clear TUI
        choice=Functions.initialMenu() #go back to start menu
    elif choice=='D': #delete list
        tests=GeneralFunctions.ListFiles('Logs','Logged Tests') #list files in Logs directory
        Functions.delTest('Logs',tests) #select and delete test
        choice=Functions.initialMenu() #go back to start menu
    else: #exit application
        break
'''

#===
#initial inputs
#===
freq_prompt='Frequency of Readings (in secs): '
freq_error='Invalid input. Please input a decimal or whole number.'
freq=input(freq+prompt) #request input for frequency of readings
freq=GeneralFunctions.checkType(float,freq_prompt,freq_error) #verify it is a number and convert it to a float
freq=GeneralFunctions.checkZero(freq,freq_prompt,freq_error) #verift it is non-zero
amount=input('Number of Readings: ')


for i in range(0,5):
    with open(cpu_temp_path,"r") as file:
        All=file.readlines()
        All[0].replace(r"\n",'')
        text=int(All[0])
        print(i)
        print(text)

'''
