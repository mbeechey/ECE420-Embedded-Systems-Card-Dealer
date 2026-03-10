import tkinter as tk

class VEGAS:

    def __init__(self): 
        
        #create window to display on LCD
        self.Gamble = tk.Tk()
        self.Gamble.geometry("480x320")

        self.titleScreenInit()


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

        self.twoPlayers = tk.Button(self.numberField, text = "2", command = self.enterPlayerCount)
        self.threePlayers = tk.Button(self.numberField, text = "3", command = self.enterPlayerCount)
        self.fourPlayers = tk.Button(self.numberField, text = "4", command = self.enterPlayerCount)
        self.fivePlayers = tk.Button(self.numberField, text = "5", command = self.enterPlayerCount)
        self.sixPlayers = tk.Button(self.numberField, text = "6", command = self.enterPlayerCount)
        self.sevenPlayers = tk.Button(self.numberField, text = "7", command = self.enterPlayerCount)
        self.eightPlayers = tk.Button(self.numberField, text = "8",command = self.enterPlayerCount)
        self.ninePlayers = tk.Button(self.numberField, text = "9", command = self.enterPlayerCount)
        self.tenPlayers = tk.Button(self.numberField, text = "10", command = self.enterPlayerCount)


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

    def gameOneSelect(self):
        print("You have selected Texas Hold Em") 
        self.purgeEverything()
        self.playerCountScreenInit()   
        


    def gameTwoSelect(self):
        print("You have selected 5 card Poker")
        self.purgeEverything()
        self.playerCountScreenInit()


    def gameThreeSelect(self):
        print("You have selected Blackjack")
        self.purgeEverything()
        self.playerCountScreenInit()


    def enterPlayerCount(self):

        print("player count set!")





VEGAS()