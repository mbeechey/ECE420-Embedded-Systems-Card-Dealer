import RPi.GPIO as GPIO
import time

IN1 = 12   # BCM 12
IN2 = 23   # BCM 23
PWM_FREQ = 1000

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm1 = GPIO.PWM(IN1, PWM_FREQ)
pwm2 = GPIO.PWM(IN2, PWM_FREQ)

pwm1.start(0)
pwm2.start(0)

print("Automatic card dealing ready")

def motor_forward(power):
    pwm2.ChangeDutyCycle(0)
    pwm1.ChangeDutyCycle(power)

def motor_reverse(power):
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(power)

def motor_stop():
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

def dispense_one_card():
    print("Forward: dispensing")
    motor_forward(95)# tune 70-100
    time.sleep(0.055)      # tune 0.05-0.18

    print("Stop")
    motor_stop()
    time.sleep(0.01) # gap before reverse

    print("Reverse: anti-double-feed")
    motor_reverse(75)    # tune 50-80
    time.sleep(0.08)      # tune 0.01-0.08

    print("Stop")
    motor_stop()
    time.sleep(1.00)  # gap before next card

try:
    while True:
        dispense_one_card()

except KeyboardInterrupt:
    print("Stopping")

finally:
    motor_stop()
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()