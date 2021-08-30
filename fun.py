##Password Generator & Storage Application
##Author: Jesse Hayward
import csv  
import datetime
import getpass
import os
import random
import string
from tkinter import Tk

## This function simply prints a nice looking splash screen for users @ cli
def WelcomeScreen():
    os.system("cls")
    print("########################################")
    print("#    Welcome to Password Generator     #")
    print("#        for Peninsula Health          #")
    print("#          by Jesse Hayward            #")
    print("########################################")
    print("\n\n-- User menu (use entry in brackets) --\n1. Generate Password (g)\n2. Review last password for user (r)\n3. Exit Console (exit)")

## This function copies the generated password into the clipboard for easy pasting into AD
def CopyToClip(password):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(password)
    r.update()
    r.destroy()

## Function for pushing latest password generation to a csv file for recalling later / auditing
def PushToCSV(password, username, system):

    ## Declare variables so we can use them dynamically through process and easier to change details later
    dateString = datetime.date.today().strftime("%d-%m-%y")
    currentUser = getpass.getuser()
    fields = [username, password, system, dateString, currentUser]

    with open('passRecord.csv', 'a+', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(fields)

## Function to print last password for a username
def PrintLastPass(username):
    Columns = ['User', 'Password', 'Sys', 'DateSet', 'AdminName']
    os.system('cls')
    print("######################################################\n\n" + str(Columns) + "\n");

    with open("passRecord.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        for lines in reader:
            if lines[0] == username:
                print(lines)

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
    return [username, length, system]

## This file runs the functions of word selector and substitutor to get a password and return it to the intial function request for a password
def GeneratePassword(passVars):

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
    PushToCSV(password, username, system)

    ##Generate in-built functional re-roll ability using recursion, avoiding oOfN Problems
    os.system('cls')
    print("######################################################");
    print("\nYour generated password is :    " + password)
    print('\n\033[4m\033[1m' + 'Password Copied to Your Clipboard' + '\033[4m\033[0m')
    passwordLiked = input("\nDid you like that password (y/n) : >> ").lower()
    if passwordLiked == 'n':
        GeneratePassword(passVars)

## This is the main menu that calls all other function in relation to user inputs and requests
def MenuAction(reply):
    if reply.lower() == "g":
        GeneratePassword(GetPassVars())
        WelcomeScreen()
    elif reply.lower() == 'r':
        username = input("Please enter the username querying >> ")
        PrintLastPass(username)
        input("Please hit enter to continue >> ")
        WelcomeScreen()
    elif reply.lower() == '':
        print("Empty input try again >> ")
    elif reply.lower() == 'exit':
        print("Thanks for using our tool :)")
    else:
        print("That's not a valid menu entry >> ")
