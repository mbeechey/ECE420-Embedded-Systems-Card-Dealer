import RPi.GPIO as GPIO
import time

# -----------------------
# DC MOTOR PINS
# -----------------------

# Chute motors (shuffling)
PWM1 = 19
DIR1 = 25

PWM2 = 13
DIR2 = 24

# Main chute motors (dispensing)
PWM3 = 12
DIR3 = 23

PWM4 = 18
DIR4 = 17

# -----------------------
# STEPPER PINS
# -----------------------

STEP_PINS = [5, 6, 16, 26]

# -----------------------
# SETUP
# -----------------------

GPIO.setmode(GPIO.BCM)

motor_pins = [PWM1, DIR1, PWM2, DIR2, PWM3, DIR3, PWM4, DIR4]

for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)

for pin in STEP_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

# PWM setup
pwm1 = GPIO.PWM(PWM1, 1000)
pwm2 = GPIO.PWM(PWM2, 1000)
pwm3 = GPIO.PWM(PWM3, 1000)
pwm4 = GPIO.PWM(PWM4, 1000)

pwm1.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

# -----------------------
# FUNCTIONS
# -----------------------

def chute1(speed):
    GPIO.output(DIR1, 0)
    pwm1.ChangeDutyCycle(speed)

def chute2(speed):
    GPIO.output(DIR2, 0)
    pwm2.ChangeDutyCycle(speed)

def main_chute(speed):
    GPIO.output(DIR3, 0)
    GPIO.output(DIR4, 0)
    pwm3.ChangeDutyCycle(speed)
    pwm4.ChangeDutyCycle(speed)

def stop_all():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)

# -----------------------
# SHUFFLE ALGORITHM
# -----------------------

def shuffle(duration=5):
    start = time.time()

    while time.time() - start < duration:
        # Quick burst from chute 1
        chute1(100)
        chute2(0)
        time.sleep(0.08)

        stop_all()
        time.sleep(0.025)

        # Quick burst from chute 2
        chute1(0)
        chute2(100)
        time.sleep(0.08)

        stop_all()
        time.sleep(0.025)

# -----------------------
# STEPPER CONTROL
# -----------------------

sequence = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]
]

def stepper_steps(steps, delay=0.0007):
    for _ in range(steps):
        for step in sequence:
            for i in range(4):
                GPIO.output(STEP_PINS[i], step[i])
            time.sleep(delay)

def main_chute_kick():
    GPIO.output(DIR3, 1)
    GPIO.output(DIR4, 1)

    # MAX POWER
    pwm3.ChangeDutyCycle(100)
    pwm4.ChangeDutyCycle(100)

    # SHORTER BURST (since you now have more power)
    time.sleep(1.5)

    # HARD STOP
    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)

# -----------------------
# MAIN PROGRAM
# -----------------------

try:
    print("Shuffling...")
    shuffle(5)

    print("Dispensing...")

    steps_per_position = 100  # adjust based on your mechanism

    for i in range(5):
        print(f"Moving to position {i+1}")
        stepper_steps(steps_per_position)
        time.sleep(0.03)
        print("Dispensing cards")
        main_chute_kick()
        time.sleep(0.2)
        time.sleep(0.5)

finally:
    stop_all()
    pwm1.stop()
    pwm2.stop()
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()