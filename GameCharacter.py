__author__ = "Samppa Raittila"
#Date: 4.12.2020

#Objects of this class are used to represent Daleks and Doctor. 
# Objects remember their coordinates and if they are living or not.
#One can classify objects giving a specific character with char attribute

class GameCharacter:
    def __init__(self,coordinates,char):
        self.__living = True
        self.__coordinates = coordinates
        self.__char = char

    def getCoordinates(self):
        return self.__coordinates

    #Function sets coordinates only if Game Character object is living
    def setCoordinates(self, coordinates):
        if self.__living:
            self.__coordinates = coordinates

    def setChar(self, char):
        self.__char = char
    
    def getChar(self):
        return self.__char
    
    def isLiving(self):
        return self.__living
        
    #Sets living to False
    def die(self):
        self.__living = False

    def __str__(self):
        return "My symbol is " + self.__char