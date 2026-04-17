import serial
import time

# Open serial port
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
time.sleep(2)  # wait for serial to settle

#universal variables for simplicity
numberPlayers = 0
gamePhase = 0
playerLocations = [0]
gameChoice = "holdthis"

print("Serial listener started, waiting for commands...")


def start_holdem():

    gamePhase = 0
    playerLocations = [0]
    initialScan(numberPlayers)
    initialDeal(2)
      

def start_5card():

    gamePhase = 0
    playerLocations = [0]
    initialScan(numberPlayers)
    initialDeal(5)
    #turn machine to first player
    goToPlayer(0)
      

def start_blackjack():

    gamePhase = 0
    playerLocations = [0]
    initialBlackjackScan(numberPlayers)
    initialDeal(2)
    #turn machine to first player
    goToPlayer(0)


def dealOneCard():
    #needs to call motors to spit out one card here
    pass

def findNextPlayer():
    #needs to use camera somehow to find next player
    pass

def goToPlayer(position):
    #rotate machine to point at player
    pass

def goToZero():
    #rotatemachine to point at Zero
    pass

def initialScan():
    for i in range(len(numberPlayers)):
        

        #standin for the moment for the camera logic, but playerLocations[i] should be whatever the next successive player's locaiton is
        playerLocations[i]=findNextPlayer()

def initialBlackjackScan():
    for i in range(len(numberPlayers)):
        
        ##Blackjack dealer always set to last player, at zero position, ensures dealer will be last dealt to and iterated to
        if (i== len(playerLocations)):
            playerLocations[len(playerLocations)] = 0

        else:
            #standin for the moment for the camera logic, but playerLocations[i] should be whatever the next successive player's locaiton is
            playerLocations[i]=findNextPlayer()


def initialDeal(numCards):
    for i in numCards:
        for j in numberPlayers:
            goToPlayer(playerLocations[j])
            dealOneCard


def nextPhase():
    if (gameChoice == "holdem"):
        nextHoldemPhase()
    elif (gameChoice == "5 card"):
        nextPokerPhase()
    elif (gameChoice == "blkjk"):
        nextBlackjackPhase()


def nextHoldemPhase():
    if (gamePhase == 0):
        goToZero()
        dealOneCard()
        dealOneCard()
        dealOneCard()
        gamePhase = gamePhase +1
    elif(gamePhase == 1):
        dealOneCard()
        dealOneCard()
        gamePhase = gamePhase +1
    elif(gamePhase == 2):
        dealOneCard()
        dealOneCard()
        gamePhase = gamePhase +1
    else:
        #this should never happen
        print("SOMETHING IS WRONG WITH HOLDEM")
        pass


def nextPokerPhase():
    #track which player is being dealt to
    gamePhase = gamePhase +1
    #turn machine to next player up
    if(gamePhase < numberPlayers):
        goToPlayer(gamePhase)
    else:
        #this should never happen
        print("SOMETHING IS WRONG WITH 5 CARD POKER")

def nextBlackjackPhase():
    #track which player is being dealt to
    gamePhase = gamePhase +1
    #turn machine to next player up (including dealer, which should be at pos 0)
    if(gamePhase < numberPlayers):
        goToPlayer(gamePhase)
    else:
        #this should never happen
        print("SOMETHING IS WRONG WITH BLACKJACK")




def handle_command(cmd):
    cmd = cmd.strip()
    print(f"Raw received: {cmd}")
    
    try:
        # Handle initial game start command from ESP32 (GAME:xxx,PLAYERS:yyy)
        if cmd.startswith("GAME:"):
            parts = cmd.split(',')
            game_part = parts[0]      # "GAME:holdem"
            players_part = parts[1]   # "PLAYERS:5"
            
            game = game_part.split(':')[1].lower().strip()
            players = int(players_part.split(':')[1])

            #pass number of players and game choice to global vars to access in game functions
            numberPlayers = players
            gameChoice = game

            ##accomodate dealer for blackjack
            if game == "blkjk":
                numberPlayers = numberPlayers +1
            
            print(f"Game mode: {game}")
            print(f"Player count: {players}")
            print(f"---")
            
            if game == "holdem":
                print("Starting Texas Hold Em")
                start_holdem()          # Call to game logic
                
            elif game == "5card":
                print("Starting 5 Card Poker")
                start_5card()           # Call to game logic
                
            elif game == "blkjk":
                print("Starting Blackjack")
                start_blackjack()       # Call to game logic
                
            else:
                print(f"Unknown game mode: {game}")
        

        elif cmd.upper() == "DEAL":
            dealOneCard()

        elif cmd.upper() == "NEXT":
            nextPhase()

        
    except Exception as e:
        print(f"Error parsing command: {e}")

# Main loop
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line:
            handle_command(line)
    time.sleep(0.1)