##Password Generator & Storage Application
##Company: Haybreaker Computing
##Author: Jesse Hayward

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

## This function copies the generated password into the clipboard for easy pasting into AD
def CopyToClip(password):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(password)
    r.update()
    r.destroy

## This function takes input and returns it
def MenuInput():
    reply = input(">> ")
    return reply

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
                if i % 5: 
                    letter = replacementNumbers[swapableLetters.index(j)]
        newLetters.append(letter)

    password = ''.join(newLetters).capitalize()

    return password

## This file runs the functions of word selector and substitutor to get a password and return it to the intial function request for a password
def GeneratePassword(length):
    
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + num + symbols

    tempPassword = RandomWordSelector(length)
    password = Substitutor(tempPassword)

    CopyToClip(password)

    return password

## This function re-runs the process if the password isn't desirable
def RegeneratePassword(length):
    password = GeneratePassword(length)
    print ('Your generated password is :    ' + password)

## This is the main menu that calls all other function in relation to user inputs and requests
def MenuAction(reply):
    if reply == "g":
        username = input("What is the user's username >> ")
        length = input("What length should the password be >> ")
        length = int(length)
        password = GeneratePassword(length)
        print("Your generated password is :    " + password)
        passwordLiked = input("Did you like that password (y/n) : >> ")
        while passwordLiked == 'n':
            RegeneratePassword(length)
            passwordLiked = input('Is this better (y/n) >> ')
        print("\n#######################################")
        print("\nThanks for using our tool")
        input("\n\nPress Enter to Continue >> ")
        WelcomeScreen()
    else:
        print("That's not a valid menu entry")
