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