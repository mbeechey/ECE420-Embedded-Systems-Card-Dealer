import RPi.GPIO as GPIO
import time

# -----------------------
# PINS (MAIN CHUTE ONLY)
# -----------------------
PWM3 = 19
DIR3 = 25

PWM4 = 18
DIR4 = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(PWM3, GPIO.OUT)
GPIO.setup(DIR3, GPIO.OUT)
GPIO.setup(PWM4, GPIO.OUT)
GPIO.setup(DIR4, GPIO.OUT)

# PWM setup
pwm3 = GPIO.PWM(PWM3, 1000)
pwm4 = GPIO.PWM(PWM4, 1000)

pwm3.start(0)
pwm4.start(0)

# -----------------------
# TEST FUNCTION
# -----------------------

def test_dispense(power=100, duration=1.0, direction=1):
    print(f"Running dispense motor | Power: {power}% | Time: {duration}s")

    GPIO.output(DIR3, direction)
    GPIO.output(DIR4, direction)

    pwm3.ChangeDutyCycle(power)
    pwm4.ChangeDutyCycle(power)

    time.sleep(duration)

    pwm3.ChangeDutyCycle(0)
    pwm4.ChangeDutyCycle(0)

    print("Stopped\n")


# -----------------------
# MAIN TEST LOOP
# -----------------------

try:
    while True:
        test_dispense(power=100, duration=1.5)
        time.sleep(2)

finally:
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()