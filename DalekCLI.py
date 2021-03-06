__author__ = "Samppa Raittila"
#Date: 4.12.2020

#Command line interface to play Dalek in terminal

import os
from time import sleep

class DalekCLI:
    def __init__(self,dalekGame):
        self.__dalekGame = dalekGame

    #Function starts the program and asks user to type in gamemap file
    #Function prints error message if there was something wrong in the file
    def startGame(self):
        self.introduce()

        while True:
            print("Give the name of the game map file which you want to play like 'boardOne.txt':")
            gamefile = input(">>> ")
            succeeded, message = self.__dalekGame.setGameboardProfessorAndDaleksFromFile(gamefile)
            if succeeded:
                break
            print(message)
            print()

        self.printGameboard()
        
        self.gameloop()

    #Function prints the Dalek banner and game instructions 
    def introduce(self):
        os.system('clear')
        introfile = open("intro.txt","r")
        for row in introfile:
            print(row, end="")
            sleep(0.1)
        introfile.close()
        print()
        print("Don't let the Daleks (A) get too near Doctor (D).")
        sleep(0.1)
        print("You can destroy Daleks by chrashing them together.")
        sleep(0.1)
        print("Chrashed Daleks (#) will not harm Doctor, but they will destroy other Daleks.")
        sleep(0.1)
        print("Move Doctor using 'w','a','s' or 'd' + Enter key")
        sleep(0.1)
        print("You can use Sonic Screwdriver by command 'ss' + Enter key.")
        sleep(0.1)
        print()
    
    #Gameloop gives user possibility to give commands and steer the Doctor. 
    #Program will break the gameloop if game ends or player presses q
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

    #Function is used to print if the player won or not
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
    