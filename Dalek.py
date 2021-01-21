__author__ = "Samppa Raittila"
#Date: 4.12.2020

#Main class for the Dalek game
#Provides possibility to choose graphical or command line interface
#Parameter "cli" chooses CLI otherwise GUI is used

from DalekGame import DalekGame 
from DalekCLI import DalekCLI
from DalekGUI import DalekGUI
import sys, getopt

def Main(argv):

    
    if len(argv) > 1:
        if argv[1]=="cli":
            game = DalekGame()
            cli = DalekCLI(game)
            cli.startGame()
        else:
            gui = DalekGUI()
    else:
        gui = DalekGUI()
        
    
    

Main(sys.argv)