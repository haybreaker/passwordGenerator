##Password Generator & Storage Application
##Company: Haybreaker Computing
##Author: Jesse Hayward

import os
import random
import string
from tkinter import Tk
import fun

##Program Runtime starts here as this is the executable main file

##Print initial startup window (splash screen)
fun.WelcomeScreen()

##Generate input for reply null-safe so it knows to run input in menu
reply = "defaultMenuInput"

##Run through menu inputs and display until exit is called
while reply != "exit":
    reply = fun.MenuInput()
    fun.MenuAction(reply)