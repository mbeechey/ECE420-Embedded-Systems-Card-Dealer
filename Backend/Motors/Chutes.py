import RPi.GPIO as GPIO
import time

# Pins
PWM_PIN = 32   # AIN1
DIR_PIN = 16   # AIN2

GPIO.setmode(GPIO.BCM)

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN, GPIO.OUT)

# Create PWM object
pwm = GPIO.PWM(PWM_PIN, 1000)  # 1kHz frequency
pwm.start(0)

try:
    print("Motor forward")

    GPIO.output(DIR_PIN, 0)   # Set direction
    pwm.ChangeDutyCycle(70)   # Speed (0-100%)

    time.sleep(5)

    print("Motor stop")
    pwm.ChangeDutyCycle(0)

    time.sleep(2)

    print("Motor reverse")

    GPIO.output(DIR_PIN, 1)
    pwm.ChangeDutyCycle(70)

    time.sleep(5)

finally:
    pwm.stop()
    GPIO.cleanup()