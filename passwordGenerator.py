## Password Generator & Storage Application
## Author: Jesse Hayward

import os
import random
import string
from tkinter import Tk
from fun2 import *

##Generate input for reply null-safe so it knows to run input in menu
reply = "defaultMenuInput"

##Print front screen then run through menu inputs and display until exit is called
WelcomeScreen()
while reply != "exit":
    reply = input(">> ")
    MenuAction(reply)