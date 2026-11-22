#===
#libraries
#===
import GeneralFunctions
import os
import time
import numpy as np
import matplotlib.pyplot as plt

SelMenuError='Invalid Response. Please input a single, capitalized letter corresponding to the action you wish to complete.'

#initial menu selection
def initialMenu():
    global SelMenuError
    GeneralFunctions.clear() #clear terminal
    GeneralFunctions.Line(30)
    GeneralFunctions.Space(1)
    options=['Run Test (R)','Plot Test (P)','Overlay Multiple Plots (O)','View Test (V)','List Tests (L)','Delete Test (D)','Exit Applications (E)'] #options list
    GeneralFunctions.VerticalList(options) #list options
    GeneralFunctions.Space(1)
    GeneralFunctions.Line(20)
    choice=str(input('Desired Action?: ')) #take action input
    while True:
        if choice=='R' or choice=='P' or choice=='O' or choice=='V' or choice=='L' or choice=='D' or choice=='E': #if choice is within valid options
            break
        else:
            print(SelMenuError) #print error message
            choice=str(input('Desired Action?: ')) #take action input
    GeneralFunctions.clear() #clear terminal
    return choice #return decision

#plotting menu
def plotMenu():
        global SelMenuError
        GeneralFunctions.clear() #clear terminal
        GeneralFunctions.Line(30)
        GeneralFunctions.Space(1)
        options=['CPU Temperature (C)','GPU Temperature (G)','Fan Speed (F)','Power Consumption (P)','Exit Plot Tool (E)'] #options list
        GeneralFunctions.VerticalList(options) #display options
        GeneralFunctions.Space(1)
        GeneralFunctions.Line(20)
        choice=str(input('Desired Plot?: ')) #take plot input
        while True:
            if choice=='C' or choice=='G' or choice=='F' or choice=='P' or choice=='E': #if choice is within valid options
                break
            else: #invalid choice
                print(SelMenuError) #print error message
                choice=str(input('Desired Plot?: ')) #take plot input
        GeneralFunctions.clear() #clear terminal
        return choice #return decision

#creates test file and parameters
def createTest():
    while True:
        frequency=0 #psuedo frequency so function does not malfunction if broken early
        measurements=0 #pseudo measurements
        decision=0 #psuedo decision
        notes=0 #psuedo notes
        #GeneralFunctions.clear()
        files=GeneralFunctions.ListFiles('Logs','Previous Tests') #list files in Logs Directory
        FileName=input('Input Test File Name, or Exit (E): ') #ask for data filename
        if FileName=='E':
            break #break function
        FileName=GeneralFunctions.RemoveCharacter(FileName,' ') #remove all spaces from name
        FileName=GeneralFunctions.EdgeCase(FileName,'Data File Name: ',' ') #verify input is not empty
        FileName+='.txt' #add suffix to name
        decision=GeneralFunctions.fileExists(FileName,'Logs',files,'Data File Name: ') #check if the file exists and if they would like to proceed
        if decision=='N':
            break
        FilePath='Logs/'+FileName #create path
        GeneralFunctions.Space(1)
        print('Please input your preferred test notes. This will not impact the operation of the test at all, and will only be visible in the top line of the subsequent file. Information that could be designated here are recommended to be test parameters, time, environmental parameters, or simple comments.') #notes message
        notes=input('Notes: ') #request input of notes
        frequency=input('Frequency of Data Recording (in seconds), or Exit (E): ') #ask for frequency of data probing
        if frequency=='E':
            break #break loop
        frequency=GeneralFunctions.checkZero(frequency,'Frequency of Data Recording (in seconds), or Exit (E): ','Invalid Input. Please input a non-zero whole number or decimal value.',float) #verify input is nonzero and a number
        measurements=input('Number of Recordings, or Exit (E): ') #ask for number of datapoints
        if measurements=='E':
            break
        measurements=GeneralFunctions.checkZero(measurements,'Number of Recordings: ','Invalid Input. Please input a non-zero whole number.',int) #verify input is nonzero and a number
        break
    return frequency,measurements,FileName,decision,notes #return relevant parameters

#selects test for plotting
def selectTest():
    GeneralFunctions.clear()
    files=GeneralFunctions.ListFiles('Logs','Logged Tests') #list files in Logs directory
    while True:
        FileName=input('Test Selection, or Exit (E): ') #ask for filename
        if FileName=='E': #if they would like to exit
            break
        if FileName not in files: #if the file does not exist
            print('Invalid Input. ['+FileName+'] does not exist. Please make sure to check your spelling and only select from the available tests listed above.') #print error message    
        else: #if file does exist
            break
    FilePath='Logs/'+FileName #create relative path
    return FilePath #return file relative path

#plots information
def plotTest(ChartLabel,units,yaxis,lower,upper,DepVar_Column,IndVar_Column=0,xaxis='Time (s)',precision=2):
    while True:
        FilePath=selectTest() #select test to plot
        if FilePath=='Logs/E': #if they would like to exit
            break
        data=np.loadtxt(FilePath, skiprows=2) #load file information into variable 'data' and skip notes and title row
        DepVar=data[:,DepVar_Column] #load dependent variable data
        avg=DepVar.mean() #calculate average parameter
        maximum=DepVar.max() #calculate maximum parameter
        minimum=DepVar.min() #calculate minimum parameter
        IndVar=data[:,IndVar_Column] #]oad independent variable data (likely time)
        GeneralFunctions.Plot(DepVar,IndVar,ChartLabel,xaxis,yaxis,lower,upper,str(round(avg,precision)),str(round(maximum,precision)),str(round(minimum,precision)),units) #plot information
        break

#plot multiple tests
def multiPlot(units,yaxis,minimum,maximum,column,precision=2):
    while True:
        choice=None #set pseudovariable that will let us exit mid operation
        files=GeneralFunctions.ListFiles('Logs','Logged Tests') #list and assign files in Logs Directory
        n=GeneralFunctions.askNumber('Number of Plots, or Exit (E): ','Invalid Input, Please input a non-zero whole number.','E',int) #ask for number of plots
        if n=='E': #if they would not like to continue
            break
        n=int(n)
        for i in range(0,n):
            while True:
                j=i+1 #institute a counter
                prompt=str(j)+'. Filename, or Exit (E): ' #prompt for each iteration
                FileName=str(input(prompt)) #ask for filename
                globals()[f"FileName{i}"]=FileName[:-4] #remove the .txt from filename and assign it to a numbered name
                if FileName in files: #if the file is in the logs directory
                    FilePath='Logs/'+FileName #specify relative filepath
                    data=np.loadtxt(FilePath,skiprows=2) #load information and ignore first two rows
                    globals()[f"time{i}"]=data[:,0] #specify time data
                    globals()[f"var{i}"]=data[:,column] #specify column of interest
                    var=globals()[f"var{i}"]
                    avg=round(var.mean(),precision) #average of parameter
                    mini=round(var.min(),precision) #minimum of parameter
                    maxi=round(var.max(),precision) #maximum of parameter
                    globals()[f"legendString{i}"]=FileName[:-4]+' | Avg: '+str(avg)+' '+units+' | Min: '+str(mini)+' '+units+' | Max: '+str(maxi)+' '+units #create legend string
                    globals()[f"avg{i}"]=avg #assign average
                    globals()[f"min{i}"]=mini #assign minimum
                    globals()[f"max{i}"]=maxi #assign maximum
                    break
                elif FileName=='E':
                    choice='end'
                    i=n #finalize count
                    break #end iterations
                else:
                    print('Invalid Input. File does not exist. Please try again.')
            if FileName=='E':
                break
        if choice=='end': #if they would not like to continue
            break
        for i in range(0,n):
            plt.plot(globals()[f"time{i}"],globals()[f"var{i}"],label=globals()[f"legendString{i}"]) #plot all stipulated plots
        plt.legend(fontsize=8) #set legend font size
        plt.xlabel("Elapsed Time (s)") #x-axis label
        plt.ylabel(yaxis) #y-axis label
        plt.ylim(minimum,maximum) #axis limits
        plt.grid(True) #show grid in plot
        plt.show() #display plot
        break #end function operation

#reads value from hwmon path and outputs as single number string
def logHWMON(path,conversionfactor=1,precision=2):
    with open(path,"r") as file: #open file as readable
        All=file.readlines() #assign all lines to a list
        All[0].replace("\n",'') #remove all extra new lines
        value=round(int(All[0])/conversionfactor,precision) #convert to base unit with rounded precision
        return str(value) #return string

#runs test with input parameters and path
def runTest(f,n,notes,filepath,cpu_path,gpu_path,fan_path,power_path,precision=2,threshold=65000):
    currentTime=0 #set current time
    with open(filepath,"a") as file: #open file as addable
        file.write(notes) #write notes to document
        file.write("\n") #go to next line
        file.write('Time(s) CPUTemperature(C) GPUTemperature(C) FanSpeed(rpm) PowerConsumption(W)') #print title of columns to document
        file.write("\n") #go to next line
    for i in range(0,n): #iterate for number of designated time points
        #record information
        currentTime=round(currentTime,precision) #round time
        cpu=logHWMON(cpu_path,1000) #record cpu temperature
        if float(cpu)>threshold: #check for outlier correction
            cpu=previouscpu #correct outlier if necessary
        gpu=logHWMON(gpu_path,1000) #record gpu temperature
        if float(gpu)>threshold:
            gpu=previousgpu
        fan=logHWMON(fan_path) #record fan speed
        if float(fan)>threshold: #if the fan is outside of reason. This is an issue where the fan will read 65535 when it begins to boost
            fan=previousfan #set it equal to the previous fan reading so the plot is smooth
        bat=logHWMON(power_path,1000000,3) #record power consumption
        if float(bat)>threshold:
            bat=previousbat
        fullreading=str(currentTime)+' '+cpu+' '+gpu+' '+fan+' '+bat #create unionized string with all readings
        #log information
        print(filepath)
        with open(filepath,"a") as file: #open file as addable
            file.write(fullreading) #document unionized string
            file.write("\n") #go to next line
        #display information
        GeneralFunctions.clear()
        GeneralFunctions.Line(30)
        print('Current Status')
        GeneralFunctions.Line(30)
        print('Progress: '+str(i+1)+'/'+str(n)) #updating progress bar
        print('Elapsed Time: '+str(currentTime)+'secs') #display current time stamp
        GeneralFunctions.Space(1)
        print('CPU Temperature: '+cpu+'C') #display cpu temperature
        print('GPU Temperature: '+gpu+'C') #display gpu temperature
        print('Fan Speed: '+fan+'rpm') #display fan speed
        print('Power Consumption: '+bat+'W') #display power consumption
        GeneralFunctions.Space(1)
        GeneralFunctions.Line(30)
        time.sleep(f) #delay for inputted amount of seconds
        currentTime+=f #increment timekeeper
        currentTIme=round(currentTime,2) #round timekeeper
        previouscpu=cpu #store previous cpu reading to eliminate outliers
        previousgpu=gpu #store previous gpu reading to eliminate outliers
        previousfan=fan #store previous fan reading to eliminate outliers
        previousbat=bat #store previous bat reading to eliminate outliers

#delete test
def delTest(logdirectory,logdirectoryfiles):
    while True: #iterate until specified otherwise
        deletion=input('File to Delete, or Exit (E): ') #ask for the file to delete
        if deletion in logdirectoryfiles: #if the file exists
            confirm=GeneralFunctions.Continue('Are you sure you would like to delete ['+deletion+']? Yes (Y) or No (N)?: ','Y','N','Invalid Input. Please input a single, capitalized letter.') #request deletion confirmation
            if confirm=='Y': #if they would like to continue
                confirm=GeneralFunctions.Continue('Are you positie that you would like to delete ['+deletion+']? This will not be recoverable if you choose to do so. Yes (Y) or No (N)?: ','Y','N','Invalid Input. Please input a single, capitalized letter.') #request second confirmation
                if confirm=='Y': #if they would like to continue
                    print('Deleting ['+deletion+'] . . .')
                    time.sleep(0.5)
                    for i in range(0,3):
                        time.sleep(0.5)
                        print('. . .')
                    file_path=logdirectory+'/'+deletion #assign file relative path
                    os.remove(file_path) #remove file
                    time.sleep(0.5)
                    print('Successfully deleted ['+deletion+'].')
                    time.sleep(0.5)
                    break
                else: #if they would not like to continue
                    break
            else: #if they would not like to continue
                break
        elif deletion=='E': #if they would not like to delete
            break
        else: #if the file is not in the logs directory
            print('Invalid Input. ['+deletion+'] does not exist. Please try again.') #error message


       
       #then we need to open up the file and output it to the file then use a new line
