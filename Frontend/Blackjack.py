import tkinter as tk

class blackJack:

    def __init__(self, playerCount): 
        
        #create window to display on LCD
        self.blackJk = tk.Tk()
        self.blackJk.geometry("480x320")

        self.scanPlayers()
        self.initialDeal()

        self.gamePhase = tk.IntVar()
        self.gamePhase = 1

        self.numPlayers = tk.IntVar()
        self.numPlayers = playerCount





        self.gameScreenInit()




        self.blackJk.mainloop()


    def gameScreenInit(self):
        #Generate label for Main menu
        self.title = tk.Label(self.blackJk, text = "Hand of Texas Hold 'Em")
        self.title.pack()


        #need to make a wide enough series of buttons to select the games
        self.buttonfield = tk.Frame(self.blackJk)
        self.buttonfield.columnconfigure(0, weight = 1)



        self.hit = tk.Button(self.buttonfield, text = "Hit", command = self.dealMoreCards)
        self.stay = tk.Button(self.buttonfield, text = "Stand", command = self.nextPlayer)

    


        self.hit.grid(row = 0, column = 0, sticky = "news")
        self.stay.grid(row = 0, column = 1, sticky = "news")

        

        self.buttonfield.pack(fill = tk.BOTH)



    def initialDeal(self):
        #PseudoCode here, not intended to work

        self.iterator = tk.IntVar()
        self.iterator = 0

        self.turnCount = tk.IntVar()
        self.turnCount = 1




            #each loop requires machine to turn to position of next player and deal a card to them
        while(self.iterator <= self.numPlayers):
            #dealer cards
            if(self.iterator == 0):
                turnToZero()
                self.dealCard()
                self.dealCard()

            self.turnToPlayer(self.iterator)
            self.dealCard()
            self.dealcard()
            self.iterator = self.iterator+1

    
    
               

    

    def dealMoreCards(self):
        
        self.turnToPlayer(self.gamePhase)
        self.dealCard()

    def nextPlayer (self):
        self.gamePhase = self.gamePhase + 1
        if(self.gamePhase > self.numPlayers):
            self.endGame()    


        


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


blackJack()