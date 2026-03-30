import RPi.GPIO as GPIO
import time

IN1 = 24
IN2 = 6
IN3 = 5
IN4 = 16

PINS = [IN1, IN2, IN3, IN4]

STEP_SEQUENCE = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1],
]

current_step = 0
step_position = 0

STEPS_PER_REV = 1280

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def step(direction=1, delay=0.002):
    global current_step, step_position
    current_step = (current_step + direction) % 4
    for i, pin in enumerate(PINS):
        GPIO.output(pin, STEP_SEQUENCE[current_step][i])
    step_position += direction
    time.sleep(delay)

def move_steps(num_steps, direction=1, delay=0.002):
    for _ in range(num_steps):
        step(direction, delay)

def motors_off():
    for pin in PINS:
        GPIO.output(pin, 0)

def cleanup():
    motors_off()
    GPIO.cleanup()

def full_360():
    print("Doing full 360 rotation...")
    move_steps(STEPS_PER_REV, direction=1)
    motors_off()
    print("Done")

def player_scan(num_players):
    steps_per_player = STEPS_PER_REV // num_players
    player_positions = {}

    print(f"Scanning for {num_players} players...")
    for i in range(1, num_players + 1):
        target = steps_per_player * i
        steps_to_move = target - step_position
        move_steps(steps_to_move, direction=1)
        motors_off()
        player_positions[i] = step_position
        print(f"Player {i} at step {step_position}")
        time.sleep(0.5)

    print("Returning to home...")
    move_steps(step_position, direction=-1)
    motors_off()
    print(f"Back at home, step {step_position}")
    return player_positions

def menu():
    setup()
    print("\n=== Stepper Menu ===")
    print("1. Full 360 rotation")
    print("2. Player scan")
    print("3. Exit")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        full_360()

    elif choice == "2":
        try:
            num = int(input("How many players (2-10)? ").strip())
            if 2 <= num <= 10:
                positions = player_scan(num)
                print(f"Player positions: {positions}")
            else:
                print("Please enter a number between 2 and 10")
        except ValueError:
            print("Invalid number")

    elif choice == "3":
        print("Exiting...")
        cleanup()
        return

    input("\nPress Enter to return to menu...")
    cleanup()
    menu()

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted")
        cleanup()