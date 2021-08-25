##Password Generator & Storage Application
##Company: Haybreaker Computing
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
    print("\n\n")
    print("1. Generate Password (g)")
    print("2. Review last password for user (r)")

## This function copies the generated password into the clipboard for easy pasting into AD
def CopyToClip(password):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(password)
    r.update()
    r.destroy

    print('\033[4m\033[1m' + 'Password Copied to Your Clipboard' + '\033[4m\033[0m')

## Function for pushing latest password generation to a csv file for recalling later / auditing
def PushToCSV(password, username, system):

    dateString = datetime.date.today().strftime("%d-%m-%y")
    currentUser = getpass.getuser()

    fields=[username, password, system, dateString, currentUser]
    with open('passRecord.csv', 'a+', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

## This function takes input and returns it
def MenuInput():
    reply = input(">> ")
    return reply

## Function to print last password for a username
def PrintLastPass(username):
    Columns = ['User', 'Password', 'Sys', 'DateSet', 'AdminName']
    os.system('cls')
    print("######################################################\n")
    print(Columns)
    print('\n')

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

    ##Go through document and get enough reads for loops for word combinations as well as single words
    ##Read number 1
    f = open('words.dat','r')
    read1 = list(f.readlines())
    f.close()
    ##Read number 2
    f = open('words.dat', 'r')
    read2 = list(f.readlines())
    f.close()

    ##Declare initial variables
    acceptableWords = list()
    for line in (read1):
        if len(line) == length: 
                acceptableWords.append(line)
                ##print(len(acceptableWords))
        for line2 in (read2):
                doubleWord = line.strip() + line2.strip()
                if len(doubleWord) == length:
                    acceptableWords.append(doubleWord)
                ##print(len(acceptableWords))

    ## Uncomment this to print all possible unaltered combinations of words print(acceptableWords)
    ##Take from the acceptable word list and choose a random
    word = random.choice(acceptableWords)
    
    ##Return the chosen word to the password generator
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
                    if swapableLetters.index(j) != 0: 
                        letter = replacementNumbers[swapableLetters.index(j)]
        newLetters.append(letter)

    return newLetters

## This file runs the functions of word selector and substitutor to get a password and return it to the intial function request for a password
def GeneratePassword(length, username, system):

    tempPassword = RandomWordSelector(length)
    passwordAsList = Substitutor(tempPassword)
    passwordAsString = ''.join(str(v) for v in Corrector(passwordAsList))
    try:
        password = passwordAsString.capitalize()
    except: 
        password = passwordAsString
        print("Password contains first letter as number, please add a Capital")

    CopyToClip(password)
    PushToCSV(password, username, system)
    return password

## This function re-runs the process if the password isn't desirable
def RegeneratePassword(length, username, system):
    password = GeneratePassword(length, username, system)
    print ('Your generated password is :    ' + password)

## This is the main menu that calls all other function in relation to user inputs and requests
def MenuAction(reply):
    if reply == "g":
        username = input("What is the user's username >> ")
        length = input("What length should the password be >> ")
        system = input("What system is this password for (AD/Clover/IPM/Etc) >> ")
        length = int(length)
        password = GeneratePassword(length, username, system)
        print("Your generated password is :    " + password)
        passwordLiked = input("Did you like that password (y/n) : >> ").lower()
        while passwordLiked == 'n':
            RegeneratePassword(length, username, system)
            passwordLiked = input('Is this better (y/n) >> ').lower()
        print("\n#######################################")
        print("\nThanks for using our tool")
        input("\n\nPress Enter to Continue >> ")
        WelcomeScreen()
    elif reply == 'r':
        username = input("Please enter the username querying >> ")
        PrintLastPass(username)
        input("Please hit enter to continue >> ")
        WelcomeScreen()
    elif reply == '':
        print("Empty input try again >> ")
    else:
        print("That's not a valid menu entry >> ")
