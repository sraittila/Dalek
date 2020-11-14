import os
from time import sleep

class DalekCLI:
    def __init__(self,dalekGame):
        self.__dalekGame = dalekGame


    def startGame(self):
        self.introduce()

        while True:
            print("Give the name of the game map file which you want to play")
            gamefile = input(">>> ")
            succeeded, message = self.__dalekGame.setGameboardProfessorAndDaleksFromFile(gamefile)
            if succeeded:
                break
            print(message)
            print()

        self.printGameboard()
        
        self.gameloop()

    
    def introduce(self):
        os.system('clear')
        introfile = open("intro.txt","r")
        for row in introfile:
            print(row, end="")
            sleep(0.1)
        introfile.close()
        print()
        print("Don't let the Daleks get too near professor.")
        sleep(0.1)
        print("You can destroy Daleks by chrashing them together.")
        sleep(0.1)
        print("Move professor using 'w','a','s' and 'd'.")
        sleep(0.1)
        print("You can use Sonic Screwdriver by command 'ss'.")
        sleep(0.1)
        print()
    

    def gameloop(self):
        while True:
            
            if self.__dalekGame.getGameIsOngoing() == False:
                break

            command = input(">>> ")

            if command=="w":
                self.__dalekGame.makeStepInGameToCoordinates(0,1)
                self.printGameboard()

            elif command=="s":
                self.__dalekGame.makeStepInGameToCoordinates(0,-1)
                self.printGameboard()

            elif command=="d":
                self.__dalekGame.makeStepInGameToCoordinates(1,0)
                self.printGameboard()

            elif command=="a":
                self.__dalekGame.makeStepInGameToCoordinates(-1,0)
                self.printGameboard()

            elif command=="ss":
                self.__dalekGame.sonicScrewdriver()
                self.printGameboard()
            
            elif command=="q":
                break

            else:
                print("You can move using w,s,a and d")

        
        self.gameResult()


    #Prints gameboard to the terminal
    def printGameboard(self):
        os.system('clear')
        gameboard = self.__dalekGame.getGameboard()
        for row in gameboard:
            for char in row:
                print(char, end="")
            print()


    def gameResult(self):
        winner = self.__dalekGame.getWinner()
        if winner == 1:
            winfile = open("youwin.txt","r")
            for row in winfile:
                print(row, end="")
                sleep(0.1)
            print()
            winfile.close()
            sleep(2)
            os.system('clear')
        elif winner == -1:
            winfile = open("youlose.txt","r")
            for row in winfile:
                print(row, end="")
                sleep(0.1)
            print()
            winfile.close()
            sleep(2)
            os.system('clear')
    