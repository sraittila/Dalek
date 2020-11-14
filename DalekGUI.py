from tkinter import *
from tkinter import messagebox
from DalekGame import DalekGame 

class DalekGUI:
    def __init__(self):
        self.__dalekGame = "dalekGame"
        self.__root = Tk()
        self.__root.title("Dalek")

        self.__startWindow = Frame(self.__root)
        self.__startCanvas = self.createStartCanvas()
        self.__startCanvas.pack()
        instructions = "Don't let the Daleks get too near Doctor. You can destroy Daleks by charshing them together. Chrashed Daleks will not harm Doctor, but they will destroy other Daleks. Move Doctor with arrow keys.You can use Sonic Screwdriver by pressing 's'.\nGood luck!"
        self.__instructions = Message(self.__startWindow, text = instructions, pady = 50, justify = CENTER)
        self.__instructions.pack()
        self.__startLabel = Label(self.__startWindow, text="Give the name of the labyrinth file:")
        self.__startLabel.pack()

        self.__fileEntry = Entry(self.__startWindow)
        self.__fileEntry.pack()

        self.__startButton = Button(self.__startWindow, text="Start game", command = self.readFile)
        self.__startButton.pack()

        self.__errorMessage = Label(self.__startWindow, text="")
        
        self.__gameWindow = Frame(self.__root)
        self.__canvas = ""

        self.__endWindow = Frame(self.__root)
        self.__endCanvas = ""
        self.__playAgain = Button(self.__endWindow, text="Play again", command = self.toStartWindow)
        
        
        self.__startWindow.pack()
        
        mainloop()

    def toStartWindow(self):
        self.__endCanvas.pack_forget()
        self.__playAgain.pack_forget()
        self.__endWindow.pack_forget()
        self.__canvas.pack_forget()
        self.__startWindow.pack()
        self.__fileEntry.delete(0, END)
        

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

    def readFile(self):
        self.__dalekGame = DalekGame()
        filename = self.__fileEntry.get()
        succeeded, message = self.__dalekGame.setGameboardProfessorAndDaleksFromFile(filename)
        if succeeded:
            self.startGame()
        else:
            messagebox.showerror("Error", message)
    
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

        
    def showWinner(self):
        self.__gameWindow.pack_forget()
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
       

    def startGame(self):
        self.__startWindow.pack_forget()
        

        self.__root.bind("<Up>",self.up)
        self.__root.bind("<Down>",self.down)
        self.__root.bind("<Left>",self.left)
        self.__root.bind("<Right>",self.right)
        self.__root.bind("s",self.sonicScrewdriver)
        
        
        
        gameboard = self.__dalekGame.getGameboard()
        w = len(gameboard[0])*25
        h = len(gameboard)*25
        
        self.__canvas = Canvas(self.__gameWindow, width=w, height=h)
        self.__canvas.pack()
        self.__gameWindow.pack()
        self.updateCanvas()



    
    def updateCanvas(self):
        
        gameboard = self.__dalekGame.getGameboard()
        self.__canvas.delete('all')
        if self.__dalekGame.getGameIsOngoing() == False:
            self.showWinner()

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
