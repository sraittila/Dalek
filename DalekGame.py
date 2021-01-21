__author__ = "Samppa Raittila"
#Date: 4.12.2020

#Class contains all the logic needed to play Dalek game.
#User interfaces can give commands to class using functions setGameboardProfessorAndDaleksFromFile(self, filename)
#makeStepInGameToCoordinates(self, x, y) and sonicScrewdriver(self). Class provides getters that can be used to get 
#all information about the game situation.


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
        gameboard = []
        #Function reads initial state and board from file
        #Function returns False if file was not found or if it wasnt
        #in the right form. Function return True if reading succeeded
        #Function returns also message describing the error
        #Game can be started when file is read succesfully
        try:
            gameBoardFile = open(filename,"r")

            firstRow = gameBoardFile.readline()
            firstRow = firstRow.strip("\n")
            rowLen = len(firstRow)

            gameBoardFile.close()

            gameBoardFile = open(filename,"r")

            for row in gameBoardFile:
                row = row.strip("\n")
                if len(row) != rowLen:
                    return False, "Rows in the file were not equal length"

                rowAsList = []
                for char in row:
                    if "*.#AD".find(char) == -1:
                        return False, "Forbidden character in the file"

                    rowAsList.append(char)
                gameboard.append(rowAsList)
            gameBoardFile.close()
        except:
            return False, "File not found"

        self.__gameboard = gameboard
        #Program searches doctor and daleks from board and initializes coordinates
        for i in range(len(self.__gameboard)):
            for j in range(len(self.__gameboard[0])):
                if self.__gameboard[i][j] == "D":
                    self.__professor.setCoordinates([i,j])
                elif self.__gameboard[i][j] == "A":
                    self.__daleks.append(GameCharacter([i,j],"A"))
                elif self.__gameboard[i][j] == "#":
                    chrashedDalek = GameCharacter([i,j], "#")
                    chrashedDalek.die()
                    self.__daleks.append(chrashedDalek)
        
        
        return True, "Succeeded"

    #Functions returns the two dimensional array that contains the updated gameboard
    def getGameboard(self):
        return self.__gameboard
    

    #Returns True if game is not finished and False if game is finished
    def getGameIsOngoing(self):
        return self.__gameIsOngoing

    #This function puts the Doctor in the random position in the gameboard
    #Function checks that Doctor doesnt land on the wall or chrashed Dalek but 
    #Doctor can land on a Dalek
    def sonicScrewdriver(self):
        if self.__gameIsOngoing:
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
            gameboard[dalekcr[0]][dalekcr[1]] = dalek.getChar()
            if dalekcr == professorcr:
                self.__professor.die()
                
        for dalek in self.__daleks:
            dalekcr = dalek.getCoordinates()
            occurancesOfSameCoordinate = dalekCoordinates.count(dalekcr)
            if occurancesOfSameCoordinate != 1:
                dalek.die()
                dalek.setChar("#")
                gameboard[dalekcr[0]][dalekcr[1]] = dalek.getChar()
        
        
        self.__gameboard = gameboard
                
            
    #Function moves Doctor in the gameboard according to x and y relative to the old coordinates 
    #Walls etc. are taken into concideration
    #For example parameters x = 1, y = 0 moves Doctor one step right
    #It will call function to move Daleks as well
    def makeStepInGameToCoordinates(self, x, y):
        if self.__gameIsOngoing:
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

    #Function moves Daleks on the board. If there is wall, function tries other directions
    #as well. Only those directions are attempted that would move Dalek closer to Doctor
    def moveDaleks(self):
        for dalek in self.__daleks:

            #coordinates = self.calculateDirection(dalek)
            coordinates = self.calculateDirectionsWithRandomBehaviour(dalek)
            i = 0
            while i < len(coordinates):
                succeeded = self.moveCharacter(coordinates[i][1],coordinates[i][0], dalek)
                if succeeded:
                    break
                i += 1
    
    #Function calculates coordinates where Daleks should attempt to move
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

    def calculateDirectionsWithRandomBehaviour(self, character):
        #Distance with sign between professor and dalek
        drow = self.__professor.getCoordinates()[0]-character.getCoordinates()[0]
        dcolumn = self.__professor.getCoordinates()[1]-character.getCoordinates()[1]
        coordinates = [[0,0]]

        absdrow = abs(drow)
        absdcolumn = abs(dcolumn)

        #If direction is obvious, directions are calculeted without random behaviour
        #using calculateDirection function
        if absdrow == absdcolumn or absdrow == 0 or absdcolumn == 0:
            return self.calculateDirection(character)

        #r is used to measure the slope of the movement
        r = 0.5
        if absdrow > absdcolumn:
            r = absdcolumn/absdrow
        else:
            r = absdrow/absdcolumn
        
        randomCoeffifent = random.random()

        #If random number is greater than r, nearest direction is calculated
        #If not, direction is calculated parallel to coordinate axis depending
        #on which coordinate is greater
        if randomCoeffifent > r:
            return self.calculateDirection(character)
        else:
            #Direction parallel to coordinate axis is chosen depending on
            #which direction takes Dalek closer to Doctor
            if absdrow > absdcolumn:
                if drow > 0:
                    coordinates[0][0] = -1
                elif drow < 0:
                    coordinates[0][0] = 1
            if absdcolumn > absdrow:
                if dcolumn > 0:
                    coordinates[0][1] = 1
                elif dcolumn < 0:
                    coordinates[0][1] = -1

        #Coordinates without random are also calculated because there could be wall in the first direction    
        extraCoordinates = self.calculateDirection(character)
        coordinates.extend(extraCoordinates)

        return coordinates





    