##Password Generator & Storage Application
##Author: Jesse Hayward
import csv  
import datetime
import getpass
import os
import pyperclip
import random
import string

##Definition of Global Variables for Potential editing and recollection
global lastPass

## This function simply prints a nice looking splash screen for users @ cli
def WelcomeScreen():
    os.system("cls")
    print("########################################")
    print("#    Welcome to Password Generator     #")
    print("#        for Peninsula Health          #")
    print("#          by Jesse Hayward            #")
    print("########################################")
    print("\n\n-- User menu (use entry in brackets) --\n1. Generate password (g)\n2. Recall last generated password (r)\n3. Exit console (exit)")

## This function copies the generated password into the clipboard for easy pasting into AD
def CopyToClip(password):
    
    pyperclip.copy(password)

## Function to print last password for a username
def PrintLastPass(lastPass):

    Columns = ['User', 'Len', 'Sys', 'Password']
    os.system('cls')
    print("######################################################\n\n" + str(Columns) + '\n\n' + str(lastPass) + "\n");
    print('\n')

## Corrector function to take final password and ensure it reaches the conditions for passwords
def Corrector(newLetters):

    containsNumber = False
    for letter in newLetters:
        if letter.isnumeric() == True:
            containsNumber = True
    if containsNumber == False: 
        newLetters.append(random.randint(1,99))
    return newLetters

## Function polls a document of 3000 entries to choose a suitbalse base dictionary word (easier to remember)
def RandomWordSelector(length):

    ##Poll Acceptable words from a document 
    f = open('words.dat').read().splitlines()
    wordLength = 0
    tempWord1 = ''; tempWord2 = ''
    while wordLength != length:
        tempWord1 = random.choice(f)
        tempWord2 = random.choice(f)
        doubleWord = tempWord1.strip() + tempWord2.strip()
        if len(tempWord1) == length:
            word = tempWord1
        if len(doubleWord) == length:
            word = doubleWord
        wordLength = len(doubleWord)

    return word

## Once a dictionary word has been selected this dictionary word gets substituted with some numbers (still human readable but harder to crack)
def Substitutor(tempPassword):

    swapableLetters = ['a', 'e', 'i', 'o', 's']
    replacementNumbers = ['4', '3', '1', '0', '5']
    newLetters = list()

    for letter in tempPassword.lower():
        for j in swapableLetters:
            if letter == j:
                i = random.randint(0,20)
                if i % 4 == 0:
                    if tempPassword.index(letter) != 0: 
                        letter = replacementNumbers[swapableLetters.index(j)]
        newLetters.append(letter)

    return newLetters

def GetPassVars():
    username = input("What is the user's username >> ")
    length = int(input("What length should the password be >> "))
    system = input("What system is this password for (AD/Clover/IPM/Etc) >> ")
    print('\n\033[4m\033[1m' + '\nCALCULATING THROUGH A HUGE NUMBER OF OPTIONS GIVE 30 SECONDS'+ '\033[4m\033[0m')
    return [username, length, system]

## This file runs the functions of word selector and substitutor to get a password and return it to the intial function request for a password
def GeneratePassword(passVars):

    global lastPass

    ## Get variables to understand password needs for the user. 
    username = str(passVars[0])
    length = int(passVars[1])
    system = str(passVars[2])
    passwordLiked = ''

    ## Go through 3 step process of randomization to build a good random password
    wordsUsed = RandomWordSelector(length)
    passwordAsList = Substitutor(wordsUsed)
    passwordAsString = ''.join(str(v) for v in Corrector(passwordAsList))
    try:
        password = passwordAsString.capitalize()
    except: 
        password = passwordAsString
        print("Password contains first letter as number, please add a Capital")
    
    CopyToClip(password)

    ##Generate in-built functional re-roll ability using recursion, avoiding oOfN Problems
    os.system('cls')
    print("######################################################");
    print("\nYour generated password is :    " + password)
    print('\n\033[4m\033[1m' + 'Password Copied to Your Clipboard' + '\033[4m\033[0m')
    passwordLiked = input("\nDid you like that password (y/n) : >> ").lower()
    lastPass = [username, length, system, password]
    if passwordLiked == 'n':
        GeneratePassword(passVars)

## This is the main menu that calls all other function in relation to user inputs and requests
def MenuAction(reply):
    global lastPass 
    if reply.lower() == "g":
        GeneratePassword(GetPassVars())
        WelcomeScreen()
    elif reply.lower() == 'r':
        try:
            PrintLastPass(lastPass)
        except:
            print("No Passwords Stored In Memory")
        input("Please hit enter to continue >> ")
        WelcomeScreen()
    elif reply.lower() == '':
        print("Empty input try again >> ")
    elif reply.lower() == 'exit':
        print("Thanks for using our tool :)")
    else:
        print("That's not a valid menu entry >> ")