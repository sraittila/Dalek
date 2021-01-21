from GameCharacter import GameCharacter
import random

class DalekGame:
    def __init__(self):
        self.__gameboard = []
        self.__professor = GameCharacter([0,0],"D")
        self.__daleks = []
        self.__gameIsOngoing = True
        self.__winner = 0
        

    def setGameboardProfessorAndDaleksFromFile(self, filename):
        #Program read initial state and board for the from file
        gameBoardFile = open(filename,"r")
        i = 0
        for row in gameBoardFile:
            row = row.strip("\n")
            rowAsList = []
            for char in row:
                rowAsList.append(char)
            self.__gameboard.append(rowAsList)
        gameBoardFile.close()

        #Program searches professor and daleks from board and initializes coordinates
        for i in range(len(self.__gameboard)):
            for j in range(len(self.__gameboard[0])):
                if self.__gameboard[i][j] == "D":
                    self.__professor.setCoordinates([i,j])
                elif self.__gameboard[i][j] == "A":
                    self.__daleks.append(GameCharacter([i,j],"A"))


    def getGameboard(self):
        return self.__gameboard
    

    #Returns True if game is not finished and False if game is finished
    def getGameIsOngoing(self):
        return self.__gameIsOngoing


    def sonicScrewdriver(self):
        while True:
            x = random.randint(0,len(self.__gameboard[0])-1)
            y = random.randint(0,len(self.__gameboard)-1)
            
            if self.__gameboard[y][x] != "*" and self.__gameboard[y][x] != "#":
                self.__professor.setCoordinates([y,x])
                break
        
        self.updateGameboard()
        self.checkIfGameIsOngoing()
          

    #Function moves character to desired coordinates if there is no wall
    #Funktion returns True if movement succeeded
    def moveCharacter(self, x ,y, character):
        oldCoordinates = character.getCoordinates()
        coordinates = [oldCoordinates[0]-y , oldCoordinates[1]+x]
        r = coordinates[0]
        c = coordinates[1]
        
        if self.__gameboard[r][c] != "*" and (character.getChar() != "D" or self.__gameboard[r][c] != "#"):
            character.setCoordinates(coordinates)
            return True

        return False


    def updateGameboard(self):
        gameboard = self.__gameboard
        
        #Initializes empty gameboard
        for i in range(len(gameboard)):
            for j in range(len(gameboard[0])):
                if gameboard[i][j] != "*":
                    gameboard[i][j] = "."
        
        #Updates position of professor
        professorcr = self.__professor.getCoordinates()
        gameboard[professorcr[0]][professorcr[1]] = "D"

        #Updates positions of daleks and checks if they have reached professor
        #Also puts coordinates of daleks in separate list
        dalekCoordinates = []
        for dalek in self.__daleks:
            dalekcr = dalek.getCoordinates()
            dalekCoordinates.append(dalekcr)
            gameboard[dalekcr[0]][dalekcr[1]] = "A"
            if dalekcr == professorcr:
                self.__professor.die()
                
        for dalek in self.__daleks:
            dalekcr = dalek.getCoordinates()
            occurancesOfSameCoordinate = dalekCoordinates.count(dalekcr)
            if occurancesOfSameCoordinate != 1:
                dalek.die()
                gameboard[dalekcr[0]][dalekcr[1]] = "#"
        
        
        self.__gameboard = gameboard
                
            
    
    def makeStepInGameToCoordinates(self, x, y):
        self.moveCharacter(x, y, self.__professor)
        self.moveDaleks()
        self.updateGameboard()
        self.checkIfGameIsOngoing()


    #checks if game is still going on returns 1 if player won
    #returns -1 if daleks won and returns 0 if game is still going
    def checkIfGameIsOngoing(self):
        if self.__professor.isLiving() == False:
            self.__gameIsOngoing = False
            self.__winner = -1
            
        
        for dalek in self.__daleks:
            if dalek.isLiving():
                return

        self.__gameIsOngoing = False
        self.__winner = 1


    def getWinner(self):
        return self.__winner


    def moveDaleks(self):
        for dalek in self.__daleks:

            coordinates = self.calculateDirection(dalek)
            i = 0
            while i < 3:
                succeeded = self.moveCharacter(coordinates[i][1],coordinates[i][0], dalek)
                if succeeded:
                    break
                i += 1
        
    def calculateDirection(self, character):
        #Distance with sign between professor and dalek
        drow = self.__professor.getCoordinates()[0]-character.getCoordinates()[0]
        dcolumn = self.__professor.getCoordinates()[1]-character.getCoordinates()[1]
        #Initializing three possible coordinates where Dalek can try to move
        possibleCoordinates = [[0,0],[0,0],[0,0]]

        #Primary direction is chosen based on the sign of the coordinates
        #If the distance is zero it means that row or column is already right
        #and coordinate will be zero as initialized
        if drow > 0:
            possibleCoordinates[0][0] = -1
        elif drow < 0:
            possibleCoordinates[0][0] = 1
        
        if dcolumn > 0:
            possibleCoordinates[0][1] = 1
        elif dcolumn < 0:
            possibleCoordinates[0][1] = -1

        #We take absolute value of distances to get idea in which direction
        #should trie to go next if it hits the wall
        absdrow = abs(drow)
        absdcolumn = abs(dcolumn)

        #If one of the values is zero it means that Dalek is going straight to
        #the wall and it shouldnt move at all
        if absdrow == 0 or absdcolumn == 0:
            return possibleCoordinates

        #Secondary and third direction is based on the comparison of absolute values
        if absdrow > absdcolumn:
            possibleCoordinates[1][0] = possibleCoordinates[0][0]
            possibleCoordinates[2][1] = possibleCoordinates[0][1]
        else:
            possibleCoordinates[1][1] = possibleCoordinates[0][1]
            possibleCoordinates[2][0] = possibleCoordinates[0][0]

        return possibleCoordinates





    