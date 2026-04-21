import serial
import time
from stepper import setup, player_scan, cleanup

# Open serial port
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
time.sleep(2)

setup()
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
            player_scan(players)
            
        elif game == "5card":
            print("Starting 5 Card Poker")
            player_scan(players)
            
        elif game == "blkjk":
            print("Starting Blackjack")
            player_scan(players)
            
    except Exception as e:
        print(f"Error parsing command: {e}")

# Main loop
try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                handle_command(line)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nInterrupted")
    cleanup()