import tkinter as tk

class FiveCard:

    def __init__(self, playerCount): 
        
        #create window to display on LCD
        self.Poker = tk.Tk()
        self.Poker.geometry("480x320")

        self.scanPlayers()
        self.initialDeal()

        self.currentPlayer = tk.IntVar()
        self.currentPlayer = 1

        self.numPlayers = tk.IntVar()
        self.numPlayers = playerCount





        self.gameScreenInit()




        self.Poker.mainloop()


    def gameScreenInit(self):
        #Generate label for Main menu
        self.title = tk.Label(self.Poker, text = "Hand of 5 Card Poker")
        self.title.pack()


        #need to make a wide enough series of buttons to select the games
        self.buttonfield = tk.Frame(self.Poker)
        self.buttonfield.columnconfigure(0, weight = 1)
        self.buttonfield.columnconfigure(1, weight = 1)


        self.game1 = tk.Button(self.buttonfield, text = "Deal Me Cards", command = self.dealMoreCards)
        self.game2 = tk.Button(self.buttonfield, text = "Next Player", command = self.iteratePlayers)
    


        self.game1.grid(row = 0, column = 0, sticky = "news")
        self.game2.grid(row = 0, column = 1, sticky = "news")
        

        self.buttonfield.pack(fill = tk.BOTH)



    def initialDeal(self):
        #PseudoCode here, not intended to work

        self.iterator = tk.IntVar()
        self.iterator = 1

        self.turnCount = tk.IntVar()
        self.turnCount = 1



        #Has to run through deals 5 tiems
        while (self.turnCount < 6):
            #each loop requires machine to turn to position of next player and deal a card to them
            while(self.iterator <= self.numPlayers):
                self.turnToPlayer(self.iterator)
                self.dealCard()
                self.iterator = self.iterator+1

            #reset to first player, iterate turncount 
            self.turnCount = self.turnCount+1
            self.iterator = 1     

    

    def dealMoreCards(self):
        self.purgeEverything()

        self.howMany = tk.Label(self.Poker, text = "How many cards do you want?")
        self.howMany.pack()

        #formatting player count selection
        self.numberField = tk.Frame(self.Poker)
        self.numberField.columnconfigure(0, weight = 1)
        self.numberField.columnconfigure(1, weight = 1)
        self.numberField.columnconfigure(2, weight = 1)


        #I can't figure out how to get these buttons to pass a value so I have to caveman brute force the values

        self.oneCard = tk.Button(self.numberField, text = "one Card", command = self.dealOneCard)
        self.twoCards = tk.Button(self.numberField, text = "two Cards", command = self.dealTwoCards)
        self.threeCards = tk.Button(self.numberField, text = "three Cards", command = self.dealThreeCards)
        self.fourCards = tk.Button(self.numberField, text = "four Cards", command = self.dealFourCards)



        self.dealOneCard.grid(row = 0, column = 0, sticky = "news")
        self.dealTwoCards.grid(row = 0, column = 1, sticky = "news")
        self.dealThreeCards.grid(row = 0, column = 2, sticky = "news")
        self.dealFourCards.grid(row = 1, column = 0, sticky = "news")


        self.numberField.pack(fill = tk.BOTH)


    def dealOneCard (self):
        #pseudocode, turn machine to player and deal cards
        self.turnToPlayer(self.currentPlayer)
        self.dealCard()

        #iterate to next player
        self.currentPlayer = self.currentPlayer +1

        #clear screen
        self.purgeEverything
        #return to hand screen
        self.gameScreenInit()

    def dealTwoCards (self):
        #pseudocode, turn machine to player and deal cards
        self.turnToPlayer(self.currentPlayer)
        self.iterator = tk.IntVar
        self.iterator = 1

        #deal two cards
        while(self.iterator < 3):
            self.dealCard()
            self.iterator = self.iterator + 1

        #iterate to next player
        self.currentPlayer = self.currentPlayer +1

        #clear screen
        self.purgeEverything
        #return to hand screen
        self.gameScreenInit()       



    def dealThreeCards (self):
        #pseudocode, turn machine to player and deal cards
        self.turnToPlayer(self.currentPlayer)
        self.iterator = tk.IntVar
        self.iterator = 1

        #deal three cards
        while(self.iterator < 4):
            self.dealCard()
            self.iterator = self.iterator + 1

        #iterate to next player
        self.currentPlayer = self.currentPlayer +1

        #clear screen
        self.purgeEverything
        #return to hand screen
        self.gameScreenInit() 

    def dealFourCards (self):
        #pseudocode, turn machine to player and deal cards
        self.turnToPlayer(self.currentPlayer)
        self.iterator = tk.IntVar
        self.iterator = 1

        #deal three cards
        while(self.iterator < 5):
            self.dealCard()
            self.iterator = self.iterator + 1

        #iterate to next player
        self.currentPlayer = self.currentPlayer +1

        #clear screen
        self.purgeEverything
        #return to hand screen
        self.gameScreenInit() 

    def iteratePlayers (self):
        self.currentPlayer = self.currentPlayer + 1
        if (self.currentPlayer > self.numPlayers):
            self.endHand()


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
                

    def purgeEverything(self):
        for widget in self.Poker.winfo_children():
            widget.destroy()


FiveCard()