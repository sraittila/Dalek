__author__ = "Samppa Raittila"
#Date: 4.12.2020

#Graphical interface to play Dalek

from tkinter import *
from tkinter import messagebox
from DalekGame import DalekGame 

class DalekGUI:
    def __init__(self):
        #Creates the root window
        self.__dalekGame = "dalekGame"
        self.__root = Tk()
        self.__root.title("Dalek")

        #Creates the start frame and instructions
        self.__startWindow = Frame(self.__root)
        self.__startCanvas = self.createStartCanvas()
        self.__startCanvas.pack()
        instructions = "Don't let the Daleks get too near Doctor (black dot). You can destroy Daleks (blue dots) by charshing them together. Chrashed Daleks (orange dots) will not harm Doctor, but they will destroy other Daleks. Move Doctor with arrow keys.You can use Sonic Screwdriver by pressing 's'.\nGood luck!"
        self.__instructions = Message(self.__startWindow, text = instructions, pady = 50, justify = CENTER)
        self.__instructions.pack()
        self.__startLabel = Label(self.__startWindow, text="Give the name of the labyrinth file like 'boardOne.txt':")
        self.__startLabel.pack()

        #Creates field where user can write file name
        self.__fileEntry = Entry(self.__startWindow)
        self.__fileEntry.pack()
        #Button to read file and start the game
        self.__startButton = Button(self.__startWindow, text="Start game", command = self.readFile)
        self.__startButton.pack()
        #Program provides error messages if file is not acceptable
        self.__errorMessage = Label(self.__startWindow, text="")
        
        #Creates the game frame and game canvas
        self.__gameWindow = Frame(self.__root)
        self.__canvas = ""
        #Creates the end frame used to show if player won or not.
        #End window includes button to return to start frame
        self.__endWindow = Frame(self.__root)
        self.__endCanvas = ""
        self.__playAgain = Button(self.__endWindow, text="Play again", command = self.toStartWindow)
        
        
        self.__startWindow.pack()
        
        mainloop()


    #Function reads file that user typed. If it succeeded, it will initialize new game and start it
    #If not, it will send error message
    def readFile(self):
        self.__dalekGame = DalekGame()
        filename = self.__fileEntry.get()
        succeeded, message = self.__dalekGame.setGameboardProfessorAndDaleksFromFile(filename)
        if succeeded:
            self.startGame()
        else:
            messagebox.showerror("Error", message)

    
        
    #Creates the Dalek text to the start frame. It reads from the file and prints square in place of *
    def createStartCanvas(self):
        introFile = self.fileToArray("intro.txt")
        w = len(introFile[0])*25
        h = len(introFile)*25
        startCanvas = Canvas(self.__startWindow, width=w, height=h)
        

        i = 0
        for row in introFile:
            j = 0
            for char in row:
                if char == "*":
                    startCanvas.create_rectangle(j,i,j+25,i+25, fill='steel blue')
                j += 25
            i += 25
        
        return startCanvas

    
    
    #Function reads textfile and puts all characters into a two dimensional array
    def fileToArray(self, filename):
        fileAsArray = []
        textfile = open(filename,"r")
        for row in textfile:
            rowAsArray = []
            row = row.strip("\n")
            for char in row:
                rowAsArray.append(char)            
            fileAsArray.append(rowAsArray)
        textfile.close()
        return fileAsArray

        
    
       
    #Function changes start frame to game frame and binds keys so that user can move in the game
    #Function creates canvas according to the size of game map that was read from a file
    def startGame(self):
        self.__startWindow.pack_forget()
        self.__gameWindow = Frame(self.__root)
        

        self.__root.bind("<Up>",self.up)
        self.__root.bind("<Down>",self.down)
        self.__root.bind("<Left>",self.left)
        self.__root.bind("<Right>",self.right)
        self.__root.bind("s",self.sonicScrewdriver)
        
        
        #Size of the gameboard is used to create proper size canvas
        gameboard = self.__dalekGame.getGameboard()
        w = len(gameboard[0])*25
        h = len(gameboard)*25
        
        self.__canvas = Canvas(self.__gameWindow, width=w, height=h)
        self.__canvas.pack()
        self.__gameWindow.pack()
        self.updateCanvas()



    #Function is used to update the game canvas after user has made a step in a game
    def updateCanvas(self):
        
        gameboard = self.__dalekGame.getGameboard()
        #If game is finished, function will call a function that shows the winner 
        if self.__dalekGame.getGameIsOngoing() == False:
            self.showWinner()
    
        self.__canvas.delete('all')

        i = 0
        for row in gameboard:
            j = 0
            for char in row:
                if char == "*":
                    self.__canvas.create_rectangle(j,i,j+25,i+25, fill='grey')
                if char == "D":
                    self.__canvas.create_oval(j,i,j+25,i+25, fill='black')
                if char == "A":
                    self.__canvas.create_oval(j,i,j+25,i+25, fill='steel blue')
                if char == "#":
                    self.__canvas.create_oval(j,i,j+25,i+25, fill='orange')
                j += 25
            i += 25


    #These five funcions are used when user moves in a game
    def up(self, event):    
        if self.__dalekGame.getGameIsOngoing():
            self.__dalekGame.makeStepInGameToCoordinates(0,1)
            self.updateCanvas()
    
    def down(self, event):
        if self.__dalekGame.getGameIsOngoing():
            self.__dalekGame.makeStepInGameToCoordinates(0,-1) 
            self.updateCanvas()
    
    def left(self, event):
        if self.__dalekGame.getGameIsOngoing():
            self.__dalekGame.makeStepInGameToCoordinates(-1,0)
            self.updateCanvas()
    
    def right(self, event):
        if self.__dalekGame.getGameIsOngoing():
            self.__dalekGame.makeStepInGameToCoordinates(1,0)
            self.updateCanvas()
    
    def sonicScrewdriver(self, event):
        if self.__dalekGame.getGameIsOngoing():
            self.__dalekGame.sonicScrewdriver()
            self.updateCanvas()

    #When game is over, this function is called and it will pack end frame and show the winner
    #It uses similiar style to read stars to squares as the update canvas and creates banner message
    def showWinner(self):
        self.__gameWindow.pack_forget()
        #self.__gameWindow.destroy()
        self.__endWindow.pack()

        winner = self.__dalekGame.getWinner()
        
        filename = ""

        if winner == 1:
            filename = "youwin.txt" 
        elif winner == -1:
            filename = "youlose.txt"
        winfileAsArray = self.fileToArray(filename)
        

        w = len(winfileAsArray[0])*25
        h = len(winfileAsArray)*25
        
        
        self.__endCanvas = Canvas(self.__endWindow, width=w, height=h)
        self.__endCanvas.pack()
        self.__playAgain.pack()
        

        i = 0
        for row in winfileAsArray:
            j = 0
            for char in row:
                if char == "*" and winner == 1:
                    self.__endCanvas.create_rectangle(j,i,j+25,i+25, fill='steel blue')
                elif char == "*" and winner == -1:
                    self.__endCanvas.create_rectangle(j,i,j+25,i+25, fill='grey')
                
                j += 25
            i += 25

    #Function is called after user has pressed play again button
    #It unpacks end frame and packs start frame
    def toStartWindow(self):
        self.__endCanvas.pack_forget()
        self.__playAgain.pack_forget()
        self.__endWindow.pack_forget()
        self.__canvas.pack_forget()
        self.__startWindow.pack()
        self.__fileEntry.delete(0, END)
