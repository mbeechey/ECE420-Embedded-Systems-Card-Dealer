import tkinter as tk

class holdEm:

    def __init__(self, playerCount): 
        
        #create window to display on LCD
        self.Poker = tk.Tk()
        self.Poker.geometry("480x320")

        self.scanPlayers()
        self.initialDeal()

        self.gamePhase = tk.IntVar()
        self.gamePhase = 1

        self.numPlayers = tk.IntVar()
        self.numPlayers = playerCount





        self.gameScreenInit()




        self.Poker.mainloop()


    def gameScreenInit(self):
        #Generate label for Main menu
        self.title = tk.Label(self.Poker, text = "Hand of Texas Hold 'Em")
        self.title.pack()


        #need to make a wide enough series of buttons to select the games
        self.buttonfield = tk.Frame(self.Poker)
        self.buttonfield.columnconfigure(0, weight = 1)



        self.game1 = tk.Button(self.buttonfield, text = "Bets Complete, start next game Phase", command = self.dealMoreCards)

    


        self.game1.grid(row = 0, column = 0, sticky = "news")

        

        self.buttonfield.pack(fill = tk.BOTH)



    def initialDeal(self):
        #PseudoCode here, not intended to work

        self.iterator = tk.IntVar()
        self.iterator = 1

        self.turnCount = tk.IntVar()
        self.turnCount = 1



        #Has to run through deals 2 times
        while (self.turnCount < 3):
            #each loop requires machine to turn to position of next player and deal a card to them
            while(self.iterator <= self.numPlayers):
                self.turnToPlayer(self.iterator)
                self.dealCard()
                self.iterator = self.iterator+1

            #reset to first player, iterate turncount 
            self.turnCount = self.turnCount+1
            self.iterator = 1     

    

    def dealMoreCards(self):
        
        self.iterator = tk.IntVar
        self.iterator = 1


        #initial deal is three cards
        if (self.phase == 1):
            while (self.iterator < 4):
                dealCard()
                self.iterator = self.iterator + 1
            self.gamePhase = self.gamePhase + 1
        elif (self.gamePhase == 2):
            dealCard()
            dealCard()
            self.gamePhase = self.gamePhase + 1
        else:
            dealCard()
            dealCard()
            self.endHand()


        self.numberField.pack(fill = tk.BOTH)


    def endHand (self):
        self.purgeEverything()

        self.replay = tk.Label(self.Poker, text = "Do you want to play again?")
        self.replay.pack()


        #need to make a wide enough series of buttons to select the games
        self.buttonfield = tk.Frame(self.Poker)
        self.buttonfield.columnconfigure(0, weight = 1)
        self.buttonfield.columnconfigure(1, weight = 1)


        self.opt1 = tk.Button(self.buttonfield, text = "Yes, new hand", command = self.__init__(self.numPlayers))
        self.opt2 = tk.Button(self.buttonfield, text = "No, Main Menu", command = self.endGame)
    


        self.opt1.grid(row = 0, column = 0, sticky = "news")
        self.opt2.grid(row = 0, column = 1, sticky = "news")
        

        self.buttonfield.pack(fill = tk.BOTH)

    def endGame (self):
        self.purgeEverything()
        self.newVegas()
        self.killProcess()




    def purgeEverything(self):
        for widget in self.Poker.winfo_children():
            widget.destroy()


holdEm()