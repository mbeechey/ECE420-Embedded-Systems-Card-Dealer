import serial
import time

# Open serial port
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
time.sleep(2)  # wait for serial to settle

print("Serial listener started, waiting for commands...")

def handle_command(cmd):
    cmd = cmd.strip()
    print(f"Raw received: {cmd}")
    
    try:
        parts = cmd.split(',')
        game = parts[0].split(':')[1]
        players = int(parts[1].split(':')[1])
        
        print(f"Game mode: {game}")
        print(f"Player count: {players}")
        print(f"---")
        
        if game == "holdem":
            print("Starting Texas Hold Em")
            # start_holdem(players)
            
        elif game == "5card":
            print("Starting 5 Card Poker")
            # start_5card(players)
            
        elif game == "blkjk":
            print("Starting Blackjack")
            # start_blackjack(players)
            
    except Exception as e:
        print(f"Error parsing command: {e}")

# Main loop
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line:
            handle_command(line)
    time.sleep(0.1)