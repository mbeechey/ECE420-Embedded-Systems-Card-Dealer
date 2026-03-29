import RPi.GPIO as GPIO
import time

# L298N pin definitions
IN1 = 24
IN2 = 6
IN3 = 5
IN4 = 16

# Step sequence for half stepping (smoother)
STEP_SEQUENCE = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1],
]

PINS = [IN1, IN2, IN3, IN4]

# Step tracking
current_step = 0
step_position = 0
player_positions = {}

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def step(direction=1, delay=0.005):
    global current_step, step_position
    current_step = (current_step + direction) % 8
    for i, pin in enumerate(PINS):
        GPIO.output(pin, STEP_SEQUENCE[current_step][i])
    step_position += direction
    time.sleep(delay)

def move_steps(num_steps, direction=1, delay=0.005):
    for _ in range(num_steps):
        step(direction, delay)

def move_to_position(target):
    global step_position
    steps_needed = target - step_position
    if steps_needed > 0:
        move_steps(steps_needed, direction=1, delay=0.005)
    elif steps_needed < 0:
        move_steps(abs(steps_needed), direction=-1, delay=0.005)

def do_360_scan():
    # 200 steps = full revolution (1.8 deg/step)
    # 8 half steps per full step = 1600 half steps per revolution
    move_steps(1600, direction=1, delay=0.005)

def reset_position():
    global step_position
    step_position = 0

def save_player_position(player_num):
    player_positions[player_num] = step_position
    print(f"Saved player {player_num} at step {step_position}")

def go_to_player(player_num):
    if player_num in player_positions:
        move_to_position(player_positions[player_num])
        print(f"At player {player_num}")

def cleanup():
    for pin in PINS:
        GPIO.output(pin, 0)
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    print("Doing 360 scan...")
    do_360_scan()
    print("Done")
    cleanup()