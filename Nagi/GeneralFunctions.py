#===
#libraries
#===
import os
import matplotlib.pyplot as plt
import time

#prints n lines of x thickness
def Line(n,x='='):
    line='' #empty line string
    for i in range(0,n): #iterate over specified length
        if x=='.': #period line
            line+='.' #elongate line string
        elif x=='-': #hyphen line
            line+='-' #elongate line string
        else: #thick line
            line+='=' #elongate line string
    print(line) #print completed string

#prints n spaces
def Space(n):
    for i in range(0,n): #iterate n times
        print('') #print empty string

#two option inquiry
def TwoOption(option1,option2,question,errorMessage):
    while True: #continue until broken
        answer=str(input(question)) #request and assign response
        if answer==option1 or answer==option2: #if answer is within permitting answers
            break #break the loop
        else: #unpermitted answer
            print(errorMessage) #error notification
    return answer #return stored response

#prints list vertically
def VerticalList(collection):
    for i in range(len(collection)): #iterate over all terms in collection
        print(collection[i]) #print each element

#verifies a variable is of a specific type and converts it
def checkType(variable,variableType,question,errorMessage):
    while True: #iterate continuously
        variable=Convert(variable,variableType)
        if type(variable) is variableType: #if of the correct type
            break #break loop
        else: #if of the incorrect type
            print(errorMessage) #print error message
            variable=input(question) #reassign input
    return variable #return convertedanswer
    
#verifies a variable is a number
def checkNumber(question,errorMessage):
    while True: #iterate continuously
        variable=input(question) #ask question
        variable=Convert(variable,float) #convert number
        if type(variable) is int or type(variable) is float: #check it is a number
            break #break loop
        else: #not number
            print(errorMessage) #print error message
    return variable #return answer

#converts to required variable type
def Convert(value,variableType):
    try:
        return variableType(value) #returns converted value
    except (ValueError, TypeError): #except when error
        return None #returns nothing

#removes character
def RemoveCharacter(string,character):
    character=str(character) #convert input character to string
    return string.replace(character,'') #return rectified string

#eliminates edge case user input when no input is passed
def NoInput(string,prompt,character=' '):
    while True: #iterate until specified otherwise
        if string=='': #if an empty string is passed
            print('Invalid input. Empty input cannot be processed')
            string=input(promp)
            string=RemoveCharacter(string,character)
        else: #if non-empty string is passed
            break #ignore and pass value
    return string #return value

#checks if input is zero
def checkZero(value,prompt,errorMessage,valueType=float):
    while True: #iterate until specified otherwise
        value=checkType(value,valueType,prompt,errorMessage) #verify and convert input into a float
        if round(float(value),2)==0.00: #value is zero
            print(errorMessage)
            value=input(prompt) #reassign value
        else: #non-zero value
            break
    return valueType(value)

#ensures an empty name is not passed
def EdgeCase(string,prompt,character):
    while True: #iterate
        if string=='':  #if an empty string is passed
            print('Invalid Input. Empty input cannot be accepted')
            string=input(prompt) #request reinput
            string=RemoveCharacter(string,character) #remove unwanted characters
        else: #if non-empty string is passed
            break
    return string #return value

#clears screen
def clear():
    print("\033[2J\033[H", end="") #clear terminal command in ASCII

#lists all files in directory
def ListFiles(directory,title):
    Line(30)
    print(title)
    Line(30)
    Space(1)
    files=[f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))] #assign all files in directory to a list
    #iterate through directory, listing all files
    for f in files:
        print(f)
    Space(1)
    Line(30)
    return files #return list of files

#ask if user would like to continue editing
def Continue(question,option1,option2,errorMessage):
    while True:
        decision=str(input(question)) #ask what they would like to do
        if decision==option1 or decision==option2: #if answer is workable
            break
        else: #if answer is not workable
            print(errorMessage)
    return decision #return decision

#checks if file exists in directory
def fileExists(name,directory,current,prompt):
    if name not in current: #if file does not exist
        confirm=Continue('Are you sure you would like to create ['+name+']? Yes (Y) or No (N)?: ','Y','N','Invalid Input. Please input a single, capitalized letter.') #request confirmation
    else: #if file already exists
        confirm=Continue('['+name+'] already exists. Would you like to overwrite this file? Yes (Y) or No (N)?: ','Y','N','Invalid Input. Please input a single, capitalized letter.') #request overwrite confirmation
        if confirm=='Y': #if they would like to overwrite
            confirm=Continue('Are you positive that you would like to delete ['+name+'] to create a new file in its place? If so, the original file will be deleted immediately after this response. Yes (Y) or No (N)? ', 'Y','N','Invalid Input. Please input a single, capitalized letter.') #request second confirmation
            if confirm=='Y': #if they would like to overwrite
                print('Deleting ['+name+'] . . .')
                time.sleep(0.5)
                for i in range(0,3):
                    time.sleep(0.5)
                    print('. . .')
                file_path=directory+'/'+name #create relative path
                os.remove(file_path) #remove old file
                time.sleep(0.5)
                print('Successfully deleted ['+name+'].')
                time.sleep(0.5)
    return confirm #return confirmation

#simple plot function
def Plot(IndVar,DepVar,ChartLabel,xaxis,yaxis,lower,upper,avg,maxi,mini,units):
    stats=ChartLabel+' | '+'Avg: '+avg+' '+units+' | '+'Min: '+mini+' '+units+' | '+'Max: '+maxi+' '+units
    plt.plot(DepVar,IndVar,color='red',label=stats) #data to plot, color, and chart title
    plt.legend(fontsize=7) #legend font size
    plt.xlabel(xaxis) #x-axis title
    plt.ylabel(yaxis) #y-axis title
    plt.ylim(lower,upper) #y-axis max and min
    plt.grid(True) #give grid
    plt.show() #display plot

#asks for a number
def askNumber(prompt,errorMessage,exitKey='E',varType=float):
    while True: #iterate until specified otherwise
        number=input(prompt) #request user input
        if number==exitKey: #if they would like to leave
            break #end loop
        number=checkZero(number,prompt,errorMessage,varType) #verify input is nonzero and of desired type
        break #end loop
    return number #return value
