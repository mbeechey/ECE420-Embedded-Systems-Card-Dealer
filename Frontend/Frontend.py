import tkinter as tk

class VEGAS:

    def __init__(self): 
        
        #create window to display on LCD
        self.Gamble = tk.Tk()
        self.Gamble.geometry("480x320")

        self.titleScreenInit()

        self.gameMode = tk.StringVar() 
        self.playerCount = tk.IntVar()



        self.Gamble.mainloop()


    def titleScreenInit(self):
        #Generate label for Main menu
        self.title = tk.Label(self.Gamble, text = "Virtual Electronic Game Automation Specialist")
        self.title.pack()


        #need to make a wide enough series of buttons to select the games
        self.optionField = tk.Frame(self.Gamble)
        self.optionField.columnconfigure(0, weight = 1)
        self.optionField.columnconfigure(1, weight = 1)
        self.optionField.columnconfigure(2, weight = 1)

        self.game1 = tk.Button(self.optionField, text = "Hold 'em", command = self.gameOneSelect)
        self.game2 = tk.Button(self.optionField, text = "5 Card Poker", command = self.gameTwoSelect)
        self.game3 = tk.Button(self.optionField, text = "Blackjack", command = self.gameThreeSelect)


        self.game1.grid(row = 0, column = 0, sticky = "news")
        self.game2.grid(row = 0, column = 1, sticky = "news")
        self.game3.grid(row = 0, column = 2, sticky = "news")

        self.optionField.pack(fill = tk.BOTH)


    def playerCountScreenInit(self):
        self.howMany = tk.Label(self.Gamble, text = "How many players would you like dealt to?")
        self.howMany.pack()

        #formatting player count selection
        self.numberField = tk.Frame(self.Gamble)
        self.numberField.columnconfigure(0, weight = 1)
        self.numberField.columnconfigure(1, weight = 1)
        self.numberField.columnconfigure(2, weight = 1)

        self.playerTotal = tk.IntVar()

        #I can't figure out how to get these buttons to pass a value so I have to caveman brute force the values

        self.twoPlayers = tk.Button(self.numberField, text = "2", command = self.enterPlayerCountTwo)
        self.threePlayers = tk.Button(self.numberField, text = "3", command = self.enterPlayerCountThree)
        self.fourPlayers = tk.Button(self.numberField, text = "4", command = self.enterPlayerCountFour)
        self.fivePlayers = tk.Button(self.numberField, text = "5", command = self.enterPlayerCountFive)
        self.sixPlayers = tk.Button(self.numberField, text = "6", command = self.enterPlayerCountSix)
        self.sevenPlayers = tk.Button(self.numberField, text = "7", command = self.enterPlayerCountSeven)
        self.eightPlayers = tk.Button(self.numberField, text = "8", command = self.enterPlayerCountEight)
        self.ninePlayers = tk.Button(self.numberField, text = "9", command = self.enterPlayerCountNine)
        self.tenPlayers = tk.Button(self.numberField, text = "10", command = self.enterPlayerCountTen)


        self.twoPlayers.grid(row = 0, column = 0, sticky = "news")
        self.threePlayers.grid(row = 0, column = 1, sticky = "news")
        self.fourPlayers.grid(row = 0, column = 2, sticky = "news")
        self.fivePlayers.grid(row = 1, column = 0, sticky = "news")
        self.sixPlayers.grid(row = 1, column = 1, sticky = "news")
        self.sevenPlayers.grid(row = 1, column = 2, sticky = "news")
        self.eightPlayers.grid(row = 2, column = 0, sticky = "news")
        self.ninePlayers.grid(row = 2, column = 1, sticky = "news")
        self.tenPlayers.grid(row = 2, column = 2, sticky = "news")

        self.numberField.pack(fill = tk.BOTH)






    def purgeEverything(self):
        for widget in self.Gamble.winfo_children():
            widget.destroy()


#Collection of gametype setting functions (SHOULD BE CONSOLIDATED EVENTUALLY)
    def gameOneSelect(self):
        print("You have selected Texas Hold Em") 
        self.purgeEverything()
        self.playerCountScreenInit()   
        self.gameMode = "holdem"
        


    def gameTwoSelect(self):
        print("You have selected 5 card Poker")
        self.purgeEverything()
        self.playerCountScreenInit()
        self.gameMode = "5card"


    def gameThreeSelect(self):
        print("You have selected Blackjack")
        self.purgeEverything()
        self.playerCountScreenInit()
        self.gameMode = "blkjk"



#Collection of player count setting Functions (SHOULD BE CONSOLIDATED EVENTUALLY)
    def enterPlayerCountTwo(self):

        self.playerCount = 2
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()

    def enterPlayerCountThree(self):

        self.playerCount = 3
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()

    def enterPlayerCountFour(self):

        self.playerCount = 4
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()

    def enterPlayerCountFive(self):

        self.playerCount = 5
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()    

    def enterPlayerCountSix(self):

        self.playerCount = 6
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()    

    def enterPlayerCountSeven(self):

        self.playerCount = 7
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()


    def enterPlayerCountEight(self):

        self.playerCount = 8
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()

    def enterPlayerCountNine(self):

        self.playerCount = 9
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()    

    def enterPlayerCountTen(self):

        self.playerCount = 10
        print("player count set!")
        print(self.playerCount)
        self.loadGameScreen()

    def loadGameScreen(self):

        self.purgeEverything()
        if self.gameMode == "holdem":
            print("We are starting Texas Holdem")
            #launch instance of holdem class window

        elif self.gameMode == "5card":
            print("We are starting a game of 5 Card Poker")
            #launch instance of poker class

        elif self.gameMode == "blkjk":
            print("We are starting a game of Blackjack")
            #launch instance of blackjack class

VEGAS()