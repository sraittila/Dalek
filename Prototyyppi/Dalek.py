from DalekGame import DalekGame 
from DalekCLI import DalekCLI

def Main():
    game = DalekGame()
    cli = DalekCLI(game)
    cli.startGame()
    

Main()