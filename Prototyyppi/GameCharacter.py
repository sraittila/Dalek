class GameCharacter:
    def __init__(self,coordinates,char):
        self.__living = True
        self.__coordinates = coordinates
        self.__char = char

    def getCoordinates(self):
        return self.__coordinates

    def setCoordinates(self, coordinates):
        if self.__living:
            self.__coordinates = coordinates

    def setChar(self, char):
        self.__char = char
    
    def getChar(self):
        return self.__char
    
    def isLiving(self):
        return self.__living
    
    def die(self):
        self.__living = False

    def __str__(self):
        return "My symbol is " + self.__char